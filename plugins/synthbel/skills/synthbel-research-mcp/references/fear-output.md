# Counterfactual output contract

The result is an evidence-grounded model judgment about answers without disclosure fear. It is neither a discovered private-belief distribution nor a correction estimated from DK alone.

## Required content

1. **Target and intervention.** Original wording and answer labels; audience, period and mode; what removing fear changes and what remains fixed. State whether the audience is observed completers or a wider population with a separate selection assumption.
2. **Observed baseline.** All original response categories, their shares and denominator, source identity and weight. Keep counts and full precision in the calculation; display sensible precision. If the baseline itself is predicted, label that first inference separately.
3. **Evidence ledger.** Source-linked observations, authors' interpretations or scenarios, and the model's own inferences. For every numerical anchor, state its population/base and why it is transportable or discounted. Retain contrary evidence and the most important missing comparison.
4. **Central recommendation.** The model's selected full distribution without fear, the change in each category in percentage points, and a short explanation of its chosen magnitude. State confidence in direction separately from magnitude; label a weakly grounded numerical choice illustrative. A zero recommendation needs an argument just as a nonzero recommendation does.
5. **Transfers and assumptions.** Which recorded categories supply each movement, how many percentage points and what fraction of each donor that represents. Label unsupported exact decompositions as judgment. Distinguish weaker evidence about the split between intensity categories from stronger evidence about grouped support or opposition.
6. **Coherent alternatives.** At least a lower-intervention and a stronger-intervention distribution when both are plausible. Each includes every original category and sums to 100%. Describe what interpretation makes it plausible, including an opposite-direction scenario when warranted. A one-sided selected set cannot rule out zero or the opposite direction. Per-option minimum/maximum values derived from these scenarios are not independent confidence bounds and cannot be combined into a new distribution.
7. **Checks and practical conclusion.** Source/denominator and arithmetic checks; the substantive conclusion that survives or changes; remaining model dependence. Report agreement or disagreement in review as robustness evidence, not accuracy against private truth.

## Quantitative mechanics

Let `p[k]` be the observed percentage in original category `k`. A chosen transfer `t[a,b]` moves percentage points from recorded category `a` to counterfactual category `b`:

`p_without_fear[k] = p[k] - sum_b t[k,b] + sum_a t[a,k]`.

Each transfer is nonnegative. The total outgoing amount from a donor cannot exceed its original mass. Keep the full original audience denominator throughout; if a contrast concerns a subgroup, convert it to the whole audience only using that subgroup's declared weight. Do not treat respondent count as a weight or multiply by an unrelated response rate.

Check that all output shares remain in [0,100] and that the total equals the original full distribution. Preserve any printed rounding residual explicitly rather than silently rescaling source figures. An observed neutral category remains substantive; genuine DK may remain after removing fear. Not-asked values are outside the eligible item base rather than donor mass.

These mechanics validate arithmetic only. They do not select the transfer magnitudes. The model selects them using the evidence ledger and states the judgment involved. There is no universal minimum, maximum or multiplier for Belarusian political questions.

## Reader-facing table

Use original answer labels in the actual assessment:

| Answer | Observed share | Model-judged change, pp | Model judgment without fear | Lower-intervention case | Stronger-intervention case |
|---|---:|---:|---:|---:|---:|
| Each original category | Recorded | Chosen and explained | Model estimate | Coherent alternative | Coherent alternative |

Label the judgment directly in chart rows and highlighted figures. Show the selected scenario range beside the central change, rather than only in collapsed detail, and call it a set of model scenarios, not an empirical bound or confidence interval. Keep the no-adjustment comparison equally visible when the evidence cannot rank it below the selected central judgment. Explain whether zero and opposite-direction changes were considered, even when absent from the selected range.

Keep the observed source date visible. A counterfactual adjustment to a historical survey is not a present-day opinion forecast. Literature or later research can inform a retrospective judgment without converting its date into today.
