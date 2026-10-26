# Portable result format, schema 1

The client performs prediction and research. The standard-library Python helper only validates arithmetic/provenance declarations and renders offline output. It never starts a model, sends data or verifies a model's actual isolation. Preserve the client's real execution identities; declarations are not independent execution receipts.

## Shared fields

Every result has `schema_version: 1`, `skill_version: "0.2.3"`, `command: "question"` or `"fear"`, and `target` with original `wording`, ordered `options` (`code` and `label` strings), `population`, and actual target `date`. `model.name` records the exposed model identity or `"unknown"`; `model.effort` is optional. Retain `release_id` from MCP, `summary`, a short `reasoning`, optional exact `digest` text and `sources` (record `id`, `title`, `date`, optional `page`, `url`, `note`). Use source locators when there is no accessible URL; never fabricate a public asset link. Preserve model-input method binding in `provenance` when available. Rendered notes should follow the user's language; original question/answer text is never translated silently.

Question and fear cards use the same fields. See the fabricated [question example](../examples/question-result.json) and [fear example](../examples/fear-result.json); these are layout fixtures, not research findings. Do not include credentials or respondent rows, even in additional metadata. Source figures, denominators and original source residuals remain explicit.

## Report-style presentation and evidence

The main plot is one stacked distribution per available result, with the original option labels and values inside its segments. Optional answer `group` values are `negative`, `positive`, `neutral`, `dk`, `refusal`, `other`; optional `strength` is `strong` or `weak`. Declare these by response meaning, never political loyalty. Only a complete yes/no mapping without substantive neutrality uses a diverging zero line. Nominal or unmapped scales use ordinary 0-100 stacks. Never manufacture a binary side or map neutrality into DK. Hatched rows distinguish comparison predictions or fear judgments from the primary/observed row; retain the accompanying labels.

`used_evidence` supplies the original corpus question cards: `id`, `wording`, `source`, `date`, optional `sample_n`, `item_n`, `population`, `mode`, `page`, original `options`, `shares`, `denominator`, `use` and `limitations`. Unknown sample/item sizes remain unreported. Partial published distributions can omit unreported codes; mark `complete_distribution: true` only for a complete 100% vector. Preserve raw source statements with `distribution_text` when numeric parsing is unavailable. No normalization or residual-category invention is permitted.

Each card's `attribution` is `explicit` when the model actually cited it, or `supplied` when it was supplied in the digest without individual attribution. The model's concise `evidence_note` and `reasoning` are displayed separately for every call. `runs[].used_evidence_ids` can name explicit source-card IDs. Resolve actual references from the answer or tool trace; do not label the entire candidate pool as used. Sources and model explanations appear side by side on wide screens and vertically on narrow screens; the exact complete digest remains accessible in its own view.

Optional `comparisons` create stacked comparison rows and result-detail tabs from already available results, not new calls. A `prediction` entry has `label` and the complete `result` in this format. An `observed` entry has `label`, original `target`, `shares`, `source` and `denominator`. Every comparison must retain exactly the target wording, ordered codes and labels. Differences in population or date require `comparability_note`, shown beside the chart; a related question does not become an observed counterpart. A failed comparison remains a failed row with no shares.

Optional `groups` entries have `label` and a complete question `result` for that explicitly defined audience. A population-group tab appears only when results exist. Use source-defined groups; do not infer respondent membership or population-wide relationships from separate marginal predictions. Comparison/group results cannot contain further comparison/group collections. Other-model and model-led-search tabs likewise appear only when supplied. Missing modes, political groups or observed surveys do not trigger hidden extra runs or empty experiment tabs.

## Question result

Add `mode`, `repeats`, `evidence_strength` (`history`, `related`, `insufficient`) and `runs`, preserving one slot for every requested prediction. Each run has `status` (`ok`, `refusal`, `no_estimate`, `invalid`, `error`), `reasoning`, optional `evidence_note`, and `shares` only when successful. Shares map exactly the original codes to finite percentages in [0,100], summing to 100 within 0.011 pp of printed rounding. Do not silently normalize invalid vectors. Record raw invalid model text privately, not as a successful card vector.

Three repeats require three distinct actual `context_id` values. In digest/neurodigest modes also record each run's `input_digest_sha256` computed from the identical exact UTF-8 `digest` text. Neurodigest always records the separate `research_context_id` and each prediction context, including a single prediction. Do not fabricate these fields when isolation cannot be established. Record `status: "unsupported"`, `runs: []` and an explanatory `reasoning` instead. A failed call in an independently started context remains its own failed slot. A technical failure before a context exists uses `status: "error"`, `execution_started: false`, `context_id: null` and its reason; no context identity is invented and no mean is produced.

The validator derives `status`, `shares` and per-category `spread` (`min`, `max`). It computes the mean only when every run succeeded. Never supply a partial mean. A three-run range describes repeat variation, not coverage or sampling uncertainty.

## Fear result

`fear.sensitivity` and `fear.mechanism` describe the question. Add `fear.design_suggestions` as useful strings. With no baseline, omit numerical results: `fear.baseline` and `fear.central` are null and `fear.alternatives` is empty. The status becomes `qualitative`.

For quantitative results, `fear.baseline` has `kind: "observed"` or `"predicted"`, `shares`, explicit `source` and `denominator`, plus `rounding_residual` if the source's printed total is not 100. Keep source date and any baseline-model identity in its metadata. A residual stays separately visible; all scenarios retain the same total and denominator rather than silently rescaling it.

`fear.central` contains the full `shares`, `rationale` and `transfers`: each transfer has `from`, `to` (original codes) and nonnegative `pp`. Outgoing mass cannot exceed the original donor. Transfers must reproduce the complete proposed central vector. An explained zero correction uses an empty transfer list.

`fear.alternatives` contains at least two coherent distributions, each with `label`, `shares` and `rationale`. Keep the no-change comparator visible when the evidence cannot favor a direction. `fear.uncertainty`, `fear.zero_considered` and `fear.opposite_considered` are explanatory strings, not booleans. Show direction and magnitude confidence separately when available. The helper derives `changes_pp`; it does not choose a correction. Extra participation scenarios need a separate explicit conditional table; the validator does not certify their selection arithmetic.

## Render or return in chat

From the installed skill directory, use:

```sh
python3 scripts/result_card.py parse '/question Example question mode=digest repeats=1'
python3 scripts/result_card.py validate RESULT.json NORMALIZED.json
python3 scripts/result_card.py render RESULT.json RESULT.html
```

Outputs must be new files. Source JSON is never overwritten. The rendered card contains its validated JSON and a download button, table copy with a selectable-text fallback, expandable explanation, exact digest, used sources and actual execution metadata. The HTML is standalone and makes no network requests. Render source strings through text nodes; do not insert model or source content as HTML. Keep the embedded JSON escaped against closing-script injection.

In an artifact-only client, attach the schema-validated result data to the bundled HTML template by replacing its single data placeholder with safely escaped JSON. If the client cannot execute the helper, check the same sums, original code sets, failures, transfers and context requirements before presentation; do not claim a Python validation receipt. If interactive HTML is unavailable, return a table with the same values, visible uncertainty and source links, followed by the same detail sections.
