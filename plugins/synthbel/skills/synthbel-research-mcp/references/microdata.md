# Microdata analysis

Use these instructions when the connected key exposes `crosstab` or `get_rows` and the research question needs joint distributions or respondent-level analysis.

Start with `browse_source` using `section: "microdata"`. Read the dataset dictionary, available variables and codes, weight, missing-value meanings, registered sample restrictions and overlapping-release metadata. Use the dataset and variable IDs actually returned by the server.

`crosstab` accepts a target `variable`, optional `by` variables and a structured `filter`. The default uses documented survey weights and the registered sample, with observed recorded answers as the denominator. Explicit DK/refusal categories remain recorded answers. `denominator: "all_eligible"` includes eligible missing mass explicitly. Keep the returned counts, weight sums, effective sample sizes, denominator definition and missingness diagnostics with the result.

If no survey weight exists, weighted analysis fails. Use `weighting: "unweighted"` only when that analysis is intended and label the result accordingly. Undocumented routing remains uncertain; blank codes alone establish neither random allocation nor an eligible answering count.

Filters use nested `all`, `any` and `not`. A leaf specifies `variable`, `op`, and `value` or `values`. Available comparisons include `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in`, `not_in`, `is_null`, `not_null`, `is_missing`, and `is_user_missing`. Supply typed source codes. The caller does not provide SQL.

Use `get_rows` for requested respondent-level analysis. Select the required 1–64 variables and filters. Its default covers all deidentified release rows; choose `base: "registered"` for the registered analysis sample. Follow every `next_cursor` with unchanged arguments and retain weights, labels and missingness metadata. Response limits may shorten a page without ending the result set. Dataset-local ordinals support variable-block alignment within the same dataset/release and do not establish linkage across waves.

The service excludes direct identifiers, interview metadata and free-text fields; field selection cannot override that policy. Every `get_rows` call is audited. Keep returned records in the researcher's authorized analysis environment; a download does not confer publication permission. Report aggregate findings with their source dependencies and limitations.
