---
name: synthbel-research-mcp
description: Predict Belarusian survey answers with /question, assess disclosure fear with /fear, and research evidence through the connected SynthBel MCP.
metadata:
  version: "0.2.5"
---

# SynthBel questions and fear

Use the user's own client model and subscription. Recommend Opus; respect another selected model. The MCP provides evidence, not model execution. Keep the actual model identity visible; use "unknown" when the client does not expose it. Never select a paid provider or install a model runner on the user's behalf.

## Choose the workflow

- `/question` or an equivalent request for an answer distribution: read [question.md](references/question.md). Defaults are `mode=digest repeats=1`; also support `mode=search`, `mode=neurodigest` and `repeats=3`.
- `/fear` or a request about disclosure sensitivity or answers without fear: read [fear-command.md](references/fear-command.md), then the maintained F procedure it links.
- Other corpus research: read [research.md](references/research.md). Use the existing eleven tools; these commands do not add server tools.

Treat the two command names as text instructions even where the client has no native slash-command menu. Natural-language requests select the same workflow. Do not claim that this archive installs native commands or connects MCP automatically.

Recover the original question, ordered options with codes, and audience from the request or its explicitly referenced source. Ask only for essential missing details; do not silently substitute another instrument or population. Preserve DK, refusal, neutrality and structural missingness separately. All-available live evidence is suitable for current research, not a held-out evaluation.

## Deliver the result

Return a short answer in the user's language and a result card following [result-format.md](references/result-format.md). Save JSON and render the shared standalone HTML with `scripts/result_card.py render INPUT.json OUTPUT.html` when file execution is available. Open it in the client's artifact or file viewer; do not publish it. With artifact support but no Python, reproduce the bundled template using the same validated JSON and DOM-safe text insertion. If HTML is unavailable, deliver the same values and expandable details as a chat table or headings. Never invent an artifact URL.

Use concise evidence-grounded explanation, not a claim to expose private model reasoning. Keep credentials and respondent rows out of cards, JSON and prompts. A numeric error, unavailable independent context or failed call stays visible rather than becoming a successful estimate. The skill version, data release, digest method and model are separate identities.
