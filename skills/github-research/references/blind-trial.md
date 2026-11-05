# Blind comparison of Skill versions

Use this procedure when evaluating whether a change to GitHub Research improves actual discovery or selection. It is a development evaluation, not a step to impose on ordinary user research. It can increase confidence across representative cases; it cannot prove field-wide recall.

## Set up a fair comparison

Choose a realistic broad research request that has not been used to write the change. Give each version the same user brief, authorized raw inputs, read-only tools, model settings when controllable, search budget, deep-read budget, and time limit. Run each version in a fresh task or equivalent isolated context. Do not give either run the desired candidates, prior reports, findings, or the change rationale. Record what the executor already knows before retrieval. If the exact task's known leads are part of the brief, provide the same list to both versions.

Pin the baseline Skill to its actual previous commit or release and record the revisions, date, tool availability, and budget. Compare both instructions against the same research date and current evidence. A current live comparison measures how the two versions behave now; it does not prove what either version would have found on its historical release date. For a historical claim, use evidence snapshots from that date. Randomize which version runs first when practical; do not reuse one run's queries or candidates in the other run.

## Compare the work

Preserve each run's actual query receipts, surfaced leads, important dispositions, inspected sources, route map, conclusion, and effort. An evaluator who did not author the change should compare:

- **Useful discovery:** decision-changing leads supported by evidence, especially leads one version found that the other did not. Deduplicate aliases and mirrors without merging meaningful forks or subcomponents.
- **Route coverage:** whether inspected candidates actually reach the requested output from the user's inputs, and what work remains with the agent, project tools, services, or user.
- **Evidence accuracy:** whether claims match the cited source and version; whether promotional copy, a demo, or a repository name was mistaken for verified behavior.
- **Cost and focus:** queries, candidates deeply inspected, elapsed effort, and recording overhead. More hits alone are not improvement; extra work should resolve a decision-relevant uncertainty.

Classify a new lead as useful only after checking the primary source and explaining how it could change the decision, constraints, or manual work. A lead that is new to one run is not automatically novel to the field. If the independent evaluator cannot determine whether a lead matters, keep it unresolved rather than awarding discovery credit. Compare both directions: useful leads and routes found only by the baseline may be regressions in the changed version, even when the new version also finds something useful.

## Interpret the outcome

A case supports the change when the new version adds independently verified, decision-relevant leads or route coverage within the same budget, preserves the baseline's important leads and accuracy, and does not add comparable losses or disproportionate effort. Record adverse changes too, such as worse source attribution, unsupported completeness claims, a baseline-only lead that changes the decision, or time spent on irrelevant platforms. If benefits and regressions offset, or the evaluator cannot establish a net advantage, call the case inconclusive and inspect the specific behavior the change was meant to improve.

Do not use a fixed candidate quota or a one-case pass as proof of recall or stability. Repeat with different real topics before making a broad quality claim. Keep the evaluation brief and outputs without expected answers in context; known-example checks can catch regressions but cannot measure blind discovery.
