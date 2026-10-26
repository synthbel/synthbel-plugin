# Tool contract

Use `tools/list` on the connected server for authoritative schemas. Both `standard` and `microdata` keys expose the nine standard tools below; `microdata` additionally exposes `crosstab` and `get_rows`. A missing tool or denied call is an access boundary, not evidence that the underlying source does not exist.

| Tool | Use |
|---|---|
| `corpus_search` | Search question meaning; optional source and group filters. Results include original wording, scales, provenance, one bounded distribution preview and the exact matching measurement count. Follow the supplied history request for all waves and groups. |
| `corpus_history` | Retrieve the exact wording and ordered-option series by `unit_id`; follow `next_cursor` to completion. Conflicting measurements remain distinct. |
| `corpus_cluster` | Find BGE-related questions. Historical cluster labels are separate descriptive metadata. |
| `list_sources` | Discover series, waves, dates, populations and coverage; follow `next_cursor` for a complete listing. |
| `browse_source` | Inspect source questions and documents; authorized `section: "microdata"` returns dictionaries and analysis views. |
| `search_findings` | Search report statements by meaning, optionally filtering type or document. Preserve type, limitations, edition and page. |
| `read_report_page` | Retrieve text using `finding_id`, or `doc_id` and a one-based `page`. Check text scope and availability. |
| `page_image` | Retrieve an authorized MCP image at the same locator. The service supplies no public bucket URL. |
| `build_packet` | Supply `unit_id`, or question wording and options with optional item, stem, population, mode and English query. Returns structured evidence and readable text, not an estimate. |
| `crosstab` | Compute weighted or explicitly unweighted distributions with grouping and structured filters; requires `microdata`. |
| `get_rows` | Retrieve selected respondent variables, weights and dictionaries with cursor pagination; requires `microdata`. |

There is no full-report-text search tool in this contract. Use source navigation, findings and page reading; report the resulting coverage limits. Other research runtimes may use different tool names, so use this server's advertised names rather than aliases from another skill.

## Completeness and units

For a paginated request, keep its arguments fixed, pass the returned cursor, and stop only when `next_cursor` is null. Cursors bind the key, release and query. If a cursor expires, restart that exact query and reconcile record IDs rather than appending duplicate pages. Keep the returned release IDs; if a research session spans releases, record that distinction before combining results.

Stored distributions and `crosstab` shares are proportions, with percentage fields where supplied. Packet shares are percentages. Use explicit units from the response and never convert twice. Empty question wording means semantic search may be unavailable; source browsing and history can still retain its categorical values.

## Digest interpretation

The serving variant `p0-bge-m3-exact-stream-live-v4` ranks the complete searchable BGE-M3 index and applies the reviewed v0.22 digest rules. Its response records the method and private rule-bundle hashes. An explicit `target_id` selects target-owned rules only when the original wording and ordered option meanings match; anonymous requests share only source-comparison notes for an exactly matching instrument. Record the actual validation receipt when claiming local digest equivalence. The client skill does not perform the controlled prediction call.

Keep source qualifications, `numeric_exclusions`, `measurement_alternatives`, `documented_representations` and the underlying records. Equal percentages do not prove duplicate observations. A recorded preferred representation is conditional on the verified source relationship and its availability; it does not merge independent samples.

The service records each call's key ID, tool, arguments, release and outcome. Credentials and returned respondent rows are excluded from those audit payloads. Use only the evidence needed for the research task.
