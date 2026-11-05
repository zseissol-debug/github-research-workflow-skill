# Opportunity lens

Use this lens to discover GitHub-native problem signals and determine whether an unresolved workflow gap deserves further validation.

## Scope boundary

GitHub is strongest for developer, maintainer, open-source adopter, and technical-workflow problems. It can reveal repeated failures, workarounds, missing integrations, maintenance burdens, and migration friction.

GitHub alone usually cannot prove market size, willingness to pay, buyer authority, or distribution access. Describe the output as an opportunity hypothesis or GitHub signal unless those external questions were separately researched.

When a commercial alternative could materially change the decision, verify it from the product's official documentation, pricing, release notes, or other primary source outside GitHub. Keep this expansion narrow and disclose it. Do not call an opportunity externally validated unless the user requested that broader research and the relevant buyer or market evidence was actually collected.

## Unit of analysis

Cluster by the user's job and failure, not by matching keywords or repository names.

A useful problem record contains:

```text
Actor and situation:
Job they are trying to complete:
Failure or friction:
Current workaround:
Consequence or urgency:
Existing alternatives:
What remains unresolved:
```

Reports that share a dependency, copied template, or upstream bug may represent one root signal. Deduplicate before judging repetition.

## Issue-first discovery

In addition to repository search, search Issues, Discussions, and PRs using vocabulary for:

- failure, limitation, missing support, manual work, workaround, migration, and repeated setup;
- requests that remain out of scope or repeatedly deferred;
- abandoned plugins, fragile scripts, and recurring integration glue;
- closed or rejected requests that reveal a deliberate product boundary;
- fixes that solved the problem and therefore weaken the opportunity.

Inspect thread context and resolution. An open Issue is not automatically an unmet need, and a closed Issue is not automatically solved.

## Triangulation

Do not use a fixed reporter-count threshold. Classify the current signal instead:

- **Hypothesis**: plausible inference or one ambiguous report.
- **Repeated GitHub signal**: distinct first-hand reports or workarounds survive deduplication.
- **Triangulated GitHub signal**: the problem appears across repositories, roles, or evidence surfaces and current alternatives remain inadequate.
- **Externally validated opportunity**: GitHub evidence is joined by credible evidence of urgency, adoption, payment, or buyer access outside GitHub.

Report the denominator and time window when available. A high Issue count without project usage or exposure context is not a frequency estimate.

## Competition and clone risk

Search for:

- native fixes and roadmap items;
- mature open-source and commercial alternatives;
- scripts or manual workflows users already accept;
- recently launched projects that cover the complete workflow;
- adjacent tools that can add the feature cheaply.

If an existing project already covers the full job, default to `Reject` unless a distinct user, workflow, distribution, or integration wedge is supported by evidence. Do not manufacture differentiation from cosmetic changes.

## Opportunity output

Lead with `Pursue`, `Keep as hypothesis`, or `Reject`, qualified by signal level.

Then show:

1. user job and concrete pain;
2. evidence and independence of the reports;
3. existing alternatives and why they do or do not close the job;
4. the unresolved gap;
5. the smallest testable wedge;
6. the next external validation step;
7. the strongest falsifier and clone risk.

Do not convert a GitHub research score into a market-size estimate. Personal constraints such as portfolio value, career fit, a 48-hour build limit, or access to interviewees belong in the request-specific brief, not in this general lens.
