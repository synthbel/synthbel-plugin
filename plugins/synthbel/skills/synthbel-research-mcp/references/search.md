# Synthetic survey estimate

Estimate how the stated Belarusian population or group would answer the supplied question now. Do not invent a target calendar date. Preserve the question's original response meanings, including don't-know when offered. The estimand is recorded survey responses, not concealed beliefs.

## Tools

Read [tool-contract.md](tool-contract.md) and inspect the connected schemas. Use `corpus_search`, `corpus_history`, `corpus_cluster`, `search_findings`, `read_report_page` and `page_image`; `browse_source` supplies navigation and methodology. This service has no full-report-text search tool. Follow all relevant history pages, retain actual fieldwork dates, and report coverage limits. It serves live evidence, without held-out evaluation exclusions.

## Procedure

1. Same question first. Search with the question wording. Among the results, take the ones whose wording and answer scale match the question and call corpus_history on the newest of them, then on the next waves back when they add a trend. This previous wave of the same question is the strongest evidence; read every measurement with its group sizes and time.
2. Related questions next. Call corpus_cluster on the best match and corpus_search with useful reformulations. Read the histories that bear on the answer: the same topic in another survey series, the same question for another population, a neighbouring item of the same battery. Use report findings or full text when the enabled tools can resolve a remaining evidence gap. Stop when further calls would not change the evidence used; any run budget is supplied by the caller.
3. Group tables when the population is a group (an age band, a sex, a region, a settlement type, an education level): take the group's row from the histories and the gap between the group and the whole sample in the earlier waves.
4. Estimate. Start from the previous wave of the same question when it exists, move it by what the related evidence and the elapsed time justify, and keep the don't-know share where earlier waves of the same scale put it. Mind the population and mode of each source (urban online panels differ from national face-to-face samples) and map options by their labels, since codes differ between surveys. With related questions only, estimate from them and say so; with no usable record, estimate from your knowledge of Belarusian survey results and say so.

## Answer

The final message is one JSON object and nothing else:

```json
{"status": "ok", "refusal_reason": null,
 "shares": {"<code>": <percent>},
 "shares_short": {"<code>": <percent>},
 "evidence": [{"unit_id": "", "source": "", "when": "", "wording": "", "shares": "", "use": ""}],
 "evidence_note": "", "reasoning": ""}
```

- `shares`: every code of the full answer scale listed in the request, percent from 0 to 100, summing to 100.
- `shares_short`: the options as asked when the request gives a short form, summing to 100 and equal to the sums of `shares` under the stated mapping; omitted otherwise.
- `evidence`: the records you used and no others, each with the unit_id the tools gave, source, time, wording, the shares you took from it and how you used it. Few records when few were relevant; an empty list when none.
- `evidence_note`: one sentence on the strength of the evidence: a previous wave of the same question, related questions only, or none.
- `reasoning`: a short note on how the estimate follows from the evidence.
- Refusal: `{"status": "refusal", "refusal_reason": "<reason>", "shares": {}, "evidence": [], "evidence_note": "", "reasoning": ""}`.

Question and option wording stay in their original language; the note and reasoning are in English. Give source time as the tools return it, including uncertainty. Follow the call's declared input and tool contract. This maintained skill describes current capabilities; frozen experiments retain their exact original prompt versions.
