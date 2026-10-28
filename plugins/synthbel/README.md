# SynthBel plugin

SynthBel helps researchers work with Belarusian public-opinion surveys. It predicts how respondents would answer a survey question, assesses whether fear could distort the recorded answers, and searches survey reports and question histories for evidence. The plugin adds instructions to your assistant and connects it to the SynthBel research server. Your own assistant subscription runs the model.

## Before you start

- A paid Claude plan (Pro, Max, Team or Enterprise) with Cowork, or a ChatGPT or Codex account with plugins.
- A personal SynthBel access key from the SynthBel team. You enter it once, on the SynthBel sign-in page. Never paste it into a chat.

## Install in Claude (Cowork)

1. Open **Customize > Plugins > Add > Add marketplace** and enter `synthbel/synthbel-plugin`.
2. Find **SynthBel** in the list and select **Install**.
3. Open the installed plugin, go to its **Connectors** tab and select **Connect**. A SynthBel page opens: enter your access key and select **Allow access** once. Respondent microdata are included when your key permits them; the option is ticked by default.

If adding a marketplace is not available to you, download `synthbel-<version>-plugin.zip` from the repository's **Releases** page and use **Customize > Plugins > Add > Upload plugin** instead. An uploaded copy does not update itself; install the newer file when a new version is announced.

## Install in Claude Code

```text
/plugin install synthbel --marketplace synthbel/synthbel-plugin
```

Then run `/mcp` and sign in to the SynthBel server.

## Install in Codex

```bash
codex plugin marketplace add synthbel/synthbel-plugin
```

```bash
codex plugin add synthbel@synthbel
```

Codex then asks you to sign in to the SynthBel connector. In the ChatGPT app, whether you can add this repository yourself depends on your account; in a company workspace an administrator may need to add it.

## Use

In Cowork, type `/` and choose **question** or **fear** from the SynthBel plugin, or simply describe what you need. In Codex, mention `$synthbel-research-mcp` or describe the task.

```text
/synthbel:question Would you support this proposal?
Options: 1 Support; 2 Oppose; 99 Difficult to say
Population: adults in Belarus
```

- **question** predicts the distribution of recorded answers, keeping "difficult to say" and refusals as separate options.
- **fear** assesses whether disclosure fear could change the answers and proposes a model-judged distribution without that fear, with alternative scenarios.
- Any other request, such as "what do surveys say about attitudes to the war?", searches the evidence.

The answer comes with a result card listing the sources used. Predictions and fear assessments are model judgments, not survey measurements.

## Data

The plugin sends your questions and search requests to the SynthBel research server and receives survey evidence from it. Your access key stays with SynthBel; the assistant receives a limited sign-in token that the SynthBel team can revoke. The plugin itself contains instructions only: no survey data, no respondent records and no credentials.

## Updates

Changes are listed in [CHANGELOG.md](CHANGELOG.md). Server (MCP) changes apply to everyone at once. Plugin (skill) changes reach you only when your copy of the plugin is updated:

- **Claude Code**: automatic updates for this marketplace are off by default. Turn them on in `/plugin` under **Marketplaces > synthbel > Enable auto-update**, or update by hand with `/plugin marketplace update synthbel`.
- **Uploaded zip**: install the newer file from the **Releases** page.

This repository is generated from the SynthBel research project; please report problems to the SynthBel team rather than editing these files.
