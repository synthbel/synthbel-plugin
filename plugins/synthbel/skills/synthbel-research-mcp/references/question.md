# Question command

Accept `/question QUESTION mode=digest repeats=1` and equivalent prose. The only execution parameters are `mode` (`digest`, `search`, `neurodigest`) and `repeats` (1 or 3). Reject other explicit values rather than guessing. `scripts/result_card.py parse` validates these parameters in a command string; wording, options and population remain model-interpreted inputs, not a rigid command grammar.

## Prepare once

Recover the question, original ordered options/codes and population. Use today's actual date unless the user explicitly asks about another period; an explicit date is a separately labelled method variant. Clarify materially ambiguous wording or audience. Do not invent options; if a source supplies them, show that instrument before using it as a replacement for missing user input. Retain any supplied short-scale mapping separately from the original scale.

Inspect tool schemas and use [tool-contract.md](tool-contract.md). Pin the returned release for the result; do not silently mix releases if the server changes during collection. No microdata access is required for the default prediction. Do not rerun deployment diagnostics or corpus-wide checks for a question.

## Select evidence and predict

**digest (default).** Call `build_packet` with the original wording/options/population, or the explicitly selected unit. `build_packet` searches earlier Belarusian questions with `wording` (most are recorded in Russian or Belarusian) and with the optional English `query_en`. Pass `wording` and option labels in the survey language: keep the user's Russian or Belarusian wording as given, and put an English rendering in `query_en`. When the user names only a topic and the selected instrument is recorded only in English, translate its wording and options into Russian for `wording`, keep the English text in `query_en`, and record the translation in the result's limitations. Never send English text as `wording` when the survey language is Russian or Belarusian. Supply `target_id` only for an exactly matching registered target. Retain `packet_body`, the complete `packet_markdown`, method binding, limitations and numeric exclusions. Read [p0-original.md](p0-original.md): these are the exact original P0 instruction bytes. Supply this instruction and `packet_markdown` to the prediction context; the packet is its complete evidence, so do not augment this mode with ad hoc retrieval. In a single-context client, use the original instruction as task guidance and identify the result as a client prediction rather than claiming a controlled system-prompt match.

**search.** Read [search.md](search.md). The prediction model itself searches comparable questions, histories and report pages while estimating. Preserve its actual used-record ledger and search limits. Do not first build a digest and relabel it model-led search. The older skill's answer object is a model response, subsequently wrapped in the common card.

**neurodigest.** First use a research context to search MCP, inspect sources, and write a source-linked digest retaining wording, dates, options, denominators, contrary evidence and limitations. Save its exact text once. A fresh prediction context receives only that frozen digest, the target and the original P0 instruction; it does not inherit the research conversation or perform further search. Use the same selected model unless the user explicitly chooses another. Retain the actual research and prediction context identities. If isolation is unavailable, explain that the requested mode cannot execute here and offer the saved digest for a new chat or an explicitly chosen supported mode; do not silently substitute one.

## Repeats and failures

One answer is the default. For `repeats=3`, start three fresh prediction contexts with identical target/model settings. `digest` and `neurodigest` reuse one frozen evidence body; `search` starts independent searches. Record actual context identities supplied by the client, not invented identifiers pretending isolation. Do not pass one prediction to another or ask a single context to pretend it is three independent models. The research context is separate from every neurodigest prediction.

Average the three full probability vectors only when all three are valid. Retain refusals, invalid responses and technical errors in their original slots; do not retry automatically, substitute zero/DK or average the successful subset. Show each result, per-option range and the mean when available. Unsupported isolation produces an explicit unsupported result rather than a fabricated run. A single answer is not the three-repeat research estimate.

## Name the result

Use "Prediction from v0.22 digest" for a client digest run, "Model-led search" for search, and "Prediction from neurodigest" for neurodigest, translated in the visible card if useful. Recommend Opus but record the actual model and known effort. An unknown model stays unknown. Claim the accepted SynthBel v0.22 configuration only with matching controlled-execution evidence; changing clients or attaching original instructions does not establish that match. Do not silently run Sol or Astra as the default.

The result contains every original option with percentages totaling 100. A source-free estimate is explicitly marked "insufficient evidence"; the model may refuse. Preserve the short explanation and the actually used sources. Return [the common result format](result-format.md); presentation happens after the prediction and never changes its shares.

## Retain the report's evidence detail

Build structured corpus question cards from the returned packet records or actual search results, preserving original options/shares, fieldwork, population, survey mode, separate sample/item sizes and bases. Match explicit references in each response to their actual records. When a supplied digest record cannot be attributed to the answer, label it supplied rather than used. Keep each call's model-on-evidence note separate from its short reasoning. The card's presentation wrapper does not change the original P0 prediction instruction.

When the user later requests another mode or model for the same instrument, retain the earlier result and add the new complete result as a comparison instead of rerunning the first. Show observed data only for a verified matching instrument, with date/audience differences explicit. Show population-group estimates when explicitly requested and available, retaining their own audience and model. Do not automatically run all modes, other models or group forecasts merely to populate report-style tabs.
