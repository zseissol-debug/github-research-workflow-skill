# Evidence matrix

Evidence strength depends on the claim being tested. Do not use a single ladder that ranks code, documentation, and user reports for every question.

## Match evidence to the claim

| Claim type | Strong evidence | Useful supporting evidence | Common false proxy |
|---|---|---|---|
| Capability | implementation path, configuration, tests, reproducible behavior, shipped Release | maintainer docs and examples | README wording alone |
| Maintenance | recent meaningful Releases, human commits, maintainer response, merged PRs, contributor continuity | published roadmap, open maintenance discussions | `pushed_at` alone |
| Adoption | dependent projects, real integrations, package or image use, recurring user activity | Stars, forks, showcase lists | Stars as user count |
| Pain or demand | independent first-hand problem reports, recurring workarounds, cross-repository corroboration | maintainer acknowledgement, reactions, repeated questions | raw Issue count |
| Reusability | source path and boundary, compatible license, dependencies, tests, minimal reproduction | examples and architecture docs | repository popularity |
| Product opportunity | repeated job-level pain, inadequate alternatives, urgency or switching evidence, external validation | GitHub problem clusters and workaround costs | Stars or complaints alone |

For product opportunity claims, GitHub can provide problem-discovery evidence but rarely proves market size, willingness to pay, or buyer access. State that boundary.

## Source classes

Label material evidence by what it is, not by a universal rank:

- **Observed**: code, configuration, API state, test result, or directly reproduced behavior.
- **Maintainer statement**: README, docs, roadmap, Release note, or maintainer comment.
- **User report**: an Issue, Discussion, comment, or independent integration report.
- **Corroborated**: mutually supporting evidence from independent actors or repositories.
- **Inference**: analysis that connects evidence but is not directly stated or observed.
- **Unknown**: a required surface that was not found, unavailable, or not tested.

Confidence is contextual:

- **High**: claim-fit evidence is direct or independently corroborated, current enough, and survives counterevidence.
- **Medium**: evidence is relevant but indirect, narrow, or missing one important surface.
- **Low**: evidence is anecdotal, stale, ambiguous, or substantially contradicted.

Within Observed evidence, distinguish static code tracing, running a repository-authored test, and an independently constructed reproduction. A passing project test proves what that test encodes; it is not automatically an independent reproduction of the user's claim.

## Joint conditions and outcome claims

Verify joint requirements along the same version, entry point, and configuration. Record the relevant input → processing → dependencies → output path when separate feature labels could hide a mismatch. A local component does not establish that the complete route is local; a model backend protocol does not automatically describe the application API.

Distinguish a mechanism from its effect: a citation field from faithful sourcing, a language interface from retrieval quality, an import from continuous synchronization, a benchmark target from measured performance. State the benchmark scope, sample, configuration, date, and who executed it. Do not turn one diagnostic into a product-wide verdict.

## Evidence ledger

Keep a compact internal record for every conclusion-changing claim:

```text
Claim:
Source class:
Source URL:
Repository and version/commit:
Published or observed date:
Retrieved date; mutable branch or pinned revision:
Validation: statement | static trace | project test | independent reproduction | untested
What it supports:
Counterevidence:
Limitations:
```

Do not expose the full ledger when a concise answer is enough, but preserve its essential fields in citations and caveats.

## Independence and deduplication

Before treating reports as repeated evidence, check whether they:

- come from distinct people or organizations;
- describe first-hand experience rather than copying another report;
- refer to separate repositories, environments, or attempts;
- share the same upstream dependency or root cause;
- predate or postdate the same fix;
- are Issues automatically created by bots or templates.

Several reports can still be one signal. Conversely, one detailed report with reproduction evidence may be more informative than many reactions.

## Contradictions and time

Prefer version-qualified conclusions. A closed Issue may mean fixed, rejected, duplicated, out of scope, or merely inactive; inspect the resolution and maintainer explanation. Search snippets may omit state. Fetch the canonical thread/API when state changes the decision, then inspect related current implementation if claiming a fix applies. A recent commit may be a bot update, documentation edit, or mechanical formatting change.

When sources disagree:

1. identify whether they refer to different versions, configurations, or user populations;
2. prefer the evidence that matches the exact claim and time window;
3. report unresolved disagreement instead of averaging it away.

## Citation discipline

Link to the narrowest source that supports the statement: a file and commit, specific Release, Issue comment, PR, or Discussion when possible. Repository homepages are insufficient citations for detailed claims.

Do not cite search-result pages as evidence. Do not let a citation sit next to a broader claim than it supports. Mark analysis that goes beyond the source as inference.

For negative findings, use bounded wording such as “not found in the inspected public exports, schema, tests, and default-branch source at commit X.” List the inspected surfaces that make the statement useful. Never shorten this to an unqualified “does not exist.”
