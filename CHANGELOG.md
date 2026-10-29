# Changelog

SynthBel has two parts, and each entry below names the part it changes.

- **Plugin (skill)**: the instructions and commands installed in your Claude or Codex client (`/synthbel:question`, `/synthbel:fear`). Its changes reach you when you update the plugin.
- **Server (MCP)**: the SynthBel research server the plugin connects to. Its changes apply to every user at once; nothing needs to be installed.

Predictions and fear assessments are model judgments, not survey measurements.

## Plugin (skill) 0.2.5 (2026-10-28)

- Digest and neurodigest predictions use a candidate instruction (`P0 v0.23 candidate`): the original instruction plus one rule. When a question asks how respondents assess negotiations with a country, the model considers separately whether attitudes toward that country are a valid guide. A negative attitude toward a country does not automatically carry over to negotiations with it. The candidate has not yet been benchmarked, and results carry its label. The previous instruction stays bundled for reproduction.
- Every digest request names a population. When none is given, the plugin uses adults in Belarus (18+) and says so in the answer.
- Result cards accept printed source percentages that sum to between 98.5 and 101.5 because of rounding. Predicted distributions must still sum to 100.

## Server (MCP) 0.1.5 (2026-10-29)

- A small number of sources are now available to the SynthBel research team only and no longer appear for partner keys in any tool: source lists, question and finding search, histories, report pages and microdata.

## Server (MCP) 0.1.4 (2026-10-28)

- Finding search results fit within client result limits. When a response would be too large, the extraction detail of the lowest-ranked findings is omitted with an explicit note; no finding is dropped, and values, wording, page and document ids are kept.
- A sign-in attempt that sends a SynthBel key as the OAuth client ID no longer records the key in the server log. The error page tells the user to re-add the connector with the client ID field empty.

## Plugin (skill) 0.2.4 (2026-10-28)

- The digest request sends the question wording in the survey language (Russian or Belarusian), with an English rendering only in `query_en`. The server finds earlier questions by that wording, so English-only wording missed directly related series.

## Server (MCP) 0.1.3 (2026-10-28)

- Question and finding search results are smaller and fit within client result limits. When a response would still be too large, the distribution previews of the lowest-ranked questions are omitted with an explicit note; no question is dropped. `corpus_history` returns the full records.
- A pagination cursor stays valid when only the page size changes.
- `browse_source` says when a source has no respondent microdata, or when a microdata dataset id was used as a source id.

## Server (MCP), 2026-10-27

- A rejected sign-in request shows the reason on the error page.

## Plugin (skill) 0.2.3 (2026-10-26)

- First public release of the plugin for Claude (Cowork, Claude Code) and Codex, with sign-in through a personal access key.
