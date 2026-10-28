#!/usr/bin/env python3
"""Validate client results and render an offline card; never call a model or MCP."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re


VERSION = "0.2.5"
MODES = {"digest", "search", "neurodigest"}
FAILURES = {"refusal", "no_estimate", "invalid", "error"}
TOLERANCE = 0.011
# Printed source percentages are rounded; a printed total of 98.5-101.5 is the source, not an error.
SOURCE_ROUNDING = 1.5


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse_command(text):
    parts = text.split()
    require(parts and parts[0] in {"/question", "/fear"}, "Expected /question or /fear")
    command = parts.pop(0)[1:]
    result = {"command": command}
    if command == "question":
        result.update(mode="digest", repeats=1)
    seen, words = set(), []
    for part in parts:
        if re.match(r"^(mode|repeats)=", part):
            key, value = part.split("=", 1)
            require(command == "question", "Execution parameters belong to /question")
            require(key not in seen, "Duplicate execution parameter")
            seen.add(key)
            require(value in (MODES if key == "mode" else {"1", "3"}), "Unsupported " + key)
            result[key] = int(value) if key == "repeats" else value
        else:
            words.append(part)
    request = " ".join(words)
    if len(request) >= 2 and request[0] == request[-1] and request[0] in {chr(34), chr(39)}:
        request = request[1:-1]
    result["request"] = request
    return result


def number(value):
    require(isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value), "Expected a finite number")
    return float(value)


def distribution(value, codes, total=100, tolerance=TOLERANCE):
    require(isinstance(value, dict) and set(value) == set(codes), "Shares must include exactly the original option codes")
    numbers = {code: number(value[code]) for code in codes}
    require(all(0 <= share <= 100 for share in numbers.values()), "Shares must lie between 0 and 100")
    require(abs(sum(numbers.values()) - total) <= tolerance, "Distribution total does not match its denominator")
    return numbers


def check_secrets(value):
    if isinstance(value, dict):
        for key, child in value.items():
            require(not re.fullmatch(r"authorization|password|api[_-]?key|(?:access|refresh)[_-]?token|(?:client[_-]?)?secret", key, re.I),
                    "Credential fields cannot enter a result card")
            check_secrets(child)
    elif isinstance(value, list):
        for child in value:
            check_secrets(child)
    elif isinstance(value, str):
        require(not re.search(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}|-----BEGIN .*PRIVATE KEY-----", value, re.I),
                "Credentials cannot enter a result card")


def validate_result(source, nested=False):
    data = copy.deepcopy(source)
    check_secrets(data)
    require(data.get("schema_version") == 1, "Unsupported result schema")
    require(data.get("skill_version") == VERSION, "Unsupported skill version")
    require(data.get("command") in {"question", "fear"}, "Unknown command")
    target = data.get("target", {})
    for key in ("wording", "population", "date"):
        require(isinstance(target.get(key), str) and target[key].strip(), "Missing target " + key)
    options = target.get("options", [])
    require(isinstance(options, list) and options, "Original options are required")
    require(all(isinstance(option, dict) and isinstance(option.get("code"), str) and option["code"]
                and isinstance(option.get("label"), str) and option["label"] for option in options), "Invalid original option")
    codes = [option["code"] for option in options]
    require(len(set(codes)) == len(codes), "Option codes must be unique")
    require(all(option.get("group") in {None, "negative", "positive", "neutral", "dk", "refusal", "other"}
                for option in options), "Unknown answer grouping")
    require(isinstance(data.get("model"), dict) and isinstance(data["model"].get("name"), str)
            and data["model"]["name"].strip(), "Record the actual model or unknown")
    require(isinstance(data.get("release_id"), str) and data["release_id"].strip(), "Record the data release or unavailable")
    if data["command"] == "question":
        validate_question(data, codes)
    else:
        validate_fear(data, codes)
    validate_evidence(data)
    comparisons, groups = data.get("comparisons", []), data.get("groups", [])
    require(data["command"] == "question" or not (comparisons or groups), "Fear scenarios belong to their explicit baseline")
    require(isinstance(comparisons, list) and isinstance(groups, list) and len(comparisons) + len(groups) <= 20,
            "Too many comparison or group rows")
    require(not nested or not (comparisons or groups), "Comparison cards cannot nest further comparisons")
    instrument = lambda value: (value["wording"], [(option["code"], option["label"]) for option in value["options"]])
    for row in comparisons:
        require(isinstance(row, dict) and row.get("label"), "Label every comparison")
        if row.get("kind") == "observed":
            require(row.get("source") and row.get("denominator"), "Observed comparisons need source and denominator")
            comparison_target = row.get("target", {})
            require(isinstance(comparison_target.get("wording"), str) and isinstance(comparison_target.get("options"), list),
                    "An observed comparison needs its original instrument")
            distribution(row.get("shares"), codes)
        else:
            require(row.get("kind") == "prediction", "Unknown comparison kind")
            result = validate_result(row.get("result", {}), nested=True)
            require(result["command"] == "question", "Compare question predictions separately from fear scenarios")
            row["result"] = result
            comparison_target = result["target"]
        require(instrument(comparison_target) == instrument(target), "Comparison instrument differs from the target")
        require(comparison_target.get("date") and comparison_target.get("population"), "Record comparison date and population")
        if any(comparison_target[key] != target[key] for key in ("date", "population")):
            require(row.get("comparability_note"), "Different comparison dates or populations require a visible qualification")
    for group in groups:
        require(isinstance(group, dict) and group.get("label"), "Label every group")
        result = validate_result(group.get("result", {}), nested=True)
        require(result["command"] == "question" and instrument(result["target"]) == instrument(target), "Group instrument differs from the question")
        group["result"] = result
    return data


def validate_evidence(data):
    records = data.get("used_evidence", [])
    require(isinstance(records, list), "Evidence records must be a list")
    identities = set()
    explicit = set()
    for record in records:
        for key in ("id", "wording", "source", "date"):
            require(isinstance(record.get(key), str) and record[key].strip(), "Missing evidence " + key)
        require(record["id"] not in identities, "Duplicate evidence identity")
        identities.add(record["id"])
        require(record.get("attribution") in {"explicit", "supplied"}, "Distinguish cited evidence from supplied digest records")
        if record.get("attribution") == "explicit":
            explicit.add(record["id"])
        if record.get("shares") is not None:
            options = record.get("options", [])
            require(all(isinstance(option, dict) and isinstance(option.get("code"), str)
                        and isinstance(option.get("label"), str) for option in options), "Preserve source option labels")
            codes = [option["code"] for option in options]
            require(codes and len(set(codes)) == len(codes), "Preserve the evidence scale")
            require(set(record["shares"]).issubset(codes), "Evidence shares contain an unknown code")
            values = [number(value) for value in record["shares"].values()]
            require(all(0 <= value <= 100 for value in values) and sum(values) <= 100 + SOURCE_ROUNDING,
                    "Invalid source shares")
            require(record.get("denominator"), "Source shares need a denominator")
            if record.get("complete_distribution"):
                distribution(record["shares"], codes, tolerance=SOURCE_ROUNDING)
            if abs(sum(values) - 100) > TOLERANCE and sum(values) > 100:
                record["printed_total"] = round(sum(values), 3)
    for run in data.get("runs", []):
        require(set(run.get("used_evidence_ids", [])).issubset(explicit), "A prediction cites an unavailable evidence record")


def validate_question(data, codes):
    mode, repeats = data.get("mode"), data.get("repeats")
    require(mode in MODES, "Unknown question mode")
    require(type(repeats) is int and repeats in {1, 3}, "Repeats must be 1 or 3")
    runs = data.get("runs", [])
    data["shares"], data["spread"] = None, None
    if data.get("status") == "unsupported":
        require(not runs and data.get("reasoning"), "Unsupported execution needs a reason and no invented runs")
        return
    require(isinstance(runs, list) and len(runs) == repeats, "Preserve every requested run slot")
    identities = []
    if mode in {"digest", "neurodigest"}:
        require(isinstance(data.get("digest"), str) and data["digest"].strip(), "The frozen digest text is required")
        digest_hash = hashlib.sha256(data["digest"].encode()).hexdigest()
        data["digest_sha256"] = digest_hash
    for run in runs:
        require(isinstance(run, dict) and run.get("status") in FAILURES | {"ok"}, "Unknown run status")
        if repeats == 3 or mode == "neurodigest":
            identity = run.get("context_id")
            if run["status"] == "error" and run.get("execution_started") is False:
                require(identity is None, "A launch failure has no invented context")
            else:
                require(isinstance(identity, str) and identity.strip(), "Actual independent context identities are required")
                identities.append(identity)
        if repeats == 3 and mode in {"digest", "neurodigest"}:
            require(run.get("input_digest_sha256") == digest_hash, "All predictions must use the same frozen digest")
        if run["status"] == "ok":
            run["shares"] = distribution(run.get("shares"), codes)
        else:
            require(run.get("shares") in (None, {}), "A failed run cannot contain a numeric prediction")
            require(run.get("reasoning"), "Preserve the refusal or failure reason")
    require(len(set(identities)) == len(identities), "Repeated contexts are not independent predictions")
    if mode == "neurodigest":
        research = data.get("research_context_id")
        require(isinstance(research, str) and research.strip() and research not in identities,
                "Research and prediction contexts must be separate")
    complete = all(run["status"] == "ok" for run in runs)
    data["status"] = "ok" if complete else "incomplete"
    if complete:
        data["shares"] = {code: sum(run["shares"][code] for run in runs) / repeats for code in codes}
        data["spread"] = {code: {"min": min(run["shares"][code] for run in runs),
                                 "max": max(run["shares"][code] for run in runs)} for code in codes}


def validate_fear(data, codes):
    fear = data.get("fear", {})
    require(isinstance(fear, dict) and isinstance(fear.get("sensitivity"), str)
            and fear["sensitivity"].strip(), "A sensitivity assessment is required")
    baseline = fear.get("baseline")
    if baseline is None:
        require(fear.get("central") is None and not fear.get("alternatives"), "Numerical F judgments require an explicit baseline")
        data["status"] = "qualitative"
        return
    require(baseline.get("kind") in {"observed", "predicted"}, "Distinguish observed and predicted baselines")
    require(baseline.get("denominator") and baseline.get("source"), "Baseline source and denominator are required")
    residual = number(baseline.get("rounding_residual", 0))
    require(abs(residual) <= 1, "Large baseline discrepancies require source reconciliation")
    original = distribution(baseline.get("shares"), codes, 100 - residual)
    central = fear.get("central", {})
    corrected = distribution(central.get("shares"), codes, sum(original.values()))
    require(central.get("rationale"), "Explain the selected correction, including a zero correction")
    outgoing = {code: 0.0 for code in codes}
    expected = dict(original)
    require(isinstance(central.get("transfers"), list), "Record central category transfers, even if empty")
    for transfer in central["transfers"]:
        donor, recipient = transfer.get("from"), transfer.get("to")
        require(donor in codes and recipient in codes and donor != recipient, "Transfers require two original categories")
        amount = number(transfer.get("pp"))
        require(amount >= 0, "Transfer amounts cannot be negative")
        outgoing[donor] += amount
        expected[donor] -= amount
        expected[recipient] += amount
    require(all(outgoing[code] <= original[code] + TOLERANCE for code in codes), "Transfer exceeds original donor mass")
    require(all(abs(expected[code] - corrected[code]) <= TOLERANCE for code in codes), "Transfers do not reproduce the central judgment")
    alternatives = fear.get("alternatives", [])
    require(isinstance(alternatives, list) and len(alternatives) >= 2, "Provide coherent lower and stronger alternatives")
    for alternative in alternatives:
        require(alternative.get("label") and alternative.get("rationale"), "Explain every alternative")
        distribution(alternative.get("shares"), codes, sum(original.values()))
    require(all(isinstance(fear.get(key), str) and fear[key].strip() for key in ("uncertainty", "zero_considered", "opposite_considered")),
            "Discuss uncertainty, zero and opposite-direction changes")
    fear["changes_pp"] = {code: corrected[code] - original[code] for code in codes}
    data["status"] = "ok"


def render_card(source):
    data = validate_result(source)
    payload = json.dumps(data, ensure_ascii=False, allow_nan=False).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    template = Path(__file__).resolve().parents[1] / "assets/result-card.html"
    return template.read_text().replace("__SYNTHBEL_RESULT__", payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("parse").add_argument("command")
    for action in ("validate", "render"):
        command = commands.add_parser(action)
        command.add_argument("input", type=Path)
        command.add_argument("output", type=Path, nargs="?" if action == "validate" else None)
    args = parser.parse_args()
    try:
        if args.action == "parse":
            print(json.dumps(parse_command(args.command)))
            return
        require(args.input.stat().st_size <= 4 * 1024 * 1024, "Result exceeds the 4 MiB card budget")
        source = json.loads(args.input.read_text())
        data = validate_result(source)
        if args.output:
            require(args.input.resolve() != args.output.resolve(), "Do not overwrite the source result")
            content = render_card(data) if args.action == "render" else json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
            with args.output.open("x") as stream:
                stream.write(content)
        print(json.dumps({"command": data["command"], "status": data["status"], "output": str(args.output) if args.output else None}))
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as error:
        parser.exit(1, "Result preparation failed: " + str(error) + "\n")


if __name__ == "__main__":
    main()
