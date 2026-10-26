# SynthBel research MCP

Use the connected service to answer the research question with recorded evidence and explicit interpretation. This skill guides research; the service retrieves evidence and calculates survey summaries. A client-generated prediction is a separate method, not an accepted SynthBel v0.22 execution.

## Establish the evidence

Inspect the connected server's tool list and schemas. Use the returned tools and scopes; a server connection does not imply microdata access. Keep credentials in the client's secure connection settings, outside requests, outputs and analysis files. For tool selection and pagination, read [tool-contract.md](tool-contract.md).

Use `list_sources` or `browse_source` when coverage or the population is unclear. For a question, start with its original wording and answer scale in `corpus_search`, inspect matching `corpus_history`, and use `corpus_cluster` or query reformulations for related evidence. Read every requested history page before describing the complete series. Preserve differently worded or ordered scales as separate comparisons.

Use `search_findings` for report evidence and `read_report_page` to check context. Inspect `page_image` when wording, a chart, a denominator or an extracted value needs verification against the rendered page. A finding's returned type distinguishes a measured result, author interpretation, methodology or limitation. State unavailable text or images explicitly. A figure quoted in report text is not the complete measurement: before reporting it, run `corpus_search` with that survey's `source_id` and report the full answer distribution from its published table or microdata record, including don't-know. Report a partial row only when that search finds no structured record, and say so.

For a supplied question and options, `build_packet` assembles a deterministic digest. For a registered local-method target, supply its explicit `target_id` and unchanged original wording, ordered options and response meanings; this enables its verified selection rules. Generic new questions receive only the applicable shared source-comparison notes. Treat matches as retrieval candidates and retain its response-base qualifications, alternative measurements and `numeric_exclusions`. For missing detail, continue through the underlying history and source tools. A resource-limit error means no complete digest was returned; use paginated tools rather than treating the error as absent evidence.

## Analyse and report

Compare original wording, answer meanings, population, mode, fieldwork and response base before combining results. Map codes by their labels. Keep don't-know, refusal, neutrality, not-asked and system missing distinct; preserve a combined source category as combined. When an item's response base is smaller than the survey sample, search the same `source_id` for a parallel wording asked of another sample split or panel before explaining the gap; report each version with its own base. If the data do not show why respondents are missing, say that the reason is unrecorded instead of guessing. Published copies, recodings and overlapping data releases do not establish independent samples or respondent linkage across waves.

For weighted crosstabs or respondent rows, first read [microdata.md](microdata.md). Aggregate distributions remain available without a microdata scope; they do not establish row access.

Answer in the user's requested format. Identify the evidence actually used, with release ID, question/record or finding IDs, source, fieldwork dates, population, relevant page and material limitations. Separate recorded observations, author interpretations and your inference. Report unavailable or incomparable evidence instead of silently removing it. A synthetic estimate is a prediction, not an additional human observation or a measure of concealed beliefs.

## Version and live-mode boundary

The skill version, server software version, served data release and prediction method are separate identities. Record the server's release, `build_packet` variant and method binding when used. A response marked `preview` is an operator test endpoint; use its comparison receipt to establish which checks passed. The endpoint provides live evidence with actual dates and no target-outcome sealing; a held-out evaluation requires its own controlled data route.

Accepted v0.22 predictions use the reviewed v0.22 digest builder, the exact original P0 instruction and the declared model and effort from the accepted run protocol. Installing this skill or passing an MCP digest to a client model does not reproduce that pipeline. If the user requests an estimate here, identify the client model and supplied evidence and label the result as a separately specified client-generated prediction; claim v0.22 only with a matching execution receipt.
