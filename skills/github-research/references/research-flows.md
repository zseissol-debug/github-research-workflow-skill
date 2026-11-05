# Research flows

Use this reference to design the search funnel and choose the depth of inspection.

## Research brief

Before collecting, express the task internally as:

```text
Decision:
Actions: Discover | Inspect | Verify
Lenses: Selection | Reuse | Opportunity | none
Targets:
Constraints:
Time window:
Depth:
Output:
```

Do not ask the user to fill this form. Infer it, state only consequential assumptions, and ask only when missing information prevents useful progress.

## Query families

Use several semantically different query families rather than minor keyword permutations:

- domain and user vocabulary;
- problem, failure, workaround, and migration vocabulary;
- implementation, protocol, library, or architecture vocabulary;
- adjacent-category and competing-workflow vocabulary;
- exclusions that remove dominant but irrelevant meanings.

Search the surfaces that fit the decision. Repository search finds projects; Issue and Discussion search finds reported problems; code search locates implementations; Releases and PRs reveal shipped behavior and maintenance decisions.

Treat the user's many required capabilities as an inspection checklist, not a single conjunctive search string. A repository description may name its purpose and underlying framework while omitting input formats, import paths, output details, or other decisive features. Try short task, workflow, or framework queries that can surface such projects; then verify the full requirement intersection in current primary sources. If a narrow all-constraints query returns little, simplify it rather than inferring that no candidate exists. Record which query exposed a decision-changing lead.

For broad discovery, phrase queries around both the user's outcome and the work that produces it. Search a few distinct vocabularies for the actual field: what users call the result, the workflow stages, and the implementation or package form. When a complementary discovery surface could reasonably surface decision-changing projects and fits the user's requested scope and access limits, use one if available, then resolve promising names, authors, or links to canonical repositories. User-supplied posts, directories, or catalogs are leads to screen, not a trusted shortlist; use them only within the user's requested scope. Do not search every platform by default or count multiple views of the same index as independent coverage. Keep the source that surfaced a decision-changing lead in its provenance.

GitHub Issue search returns pull requests unless the query includes `is:issue`. Add `is:pr` when deliberately searching pull requests. Treat search ranking as retrieval order, not evidence quality.

## Adaptive funnel

### Landscape

For broad discovery, sketch the path from the user's actual inputs to the requested result, including steps still supplied by the user or host. Split a bundled input only where its alternatives imply different transformations or outputs; do not count file-format acceptance as completion of the user's job. As early candidates emerge, check whether they merely offer variations of the same path. Before spending most inspection effort on those candidates, pursue a different plausible route if it could remove substantial preparation, change the output, or satisfy a material constraint. This is an adaptive check, not a fixed taxonomy or a requirement to finish discovery before reading any code.

Derive follow-up queries from the unresolved step or mechanism, rather than only adding known product names. Promising dependencies, authors, adjacent workflows, and community terminology can expose alternatives. A named dependency is a lead, not proof that its direct workflow has been compared. Follow it only when that comparison could matter; do not recursively audit an ecosystem. Record the question an extension is meant to resolve. Related clients of one backend do not count as different evidence; web content search may complement repository metadata search.

If result ordering repeatedly surfaces established projects while plausible new or low-attention routes remain open, change the query, sort, or use justified non-overlapping Star/date partitions and record their boundaries. A query with no minimum Star filter alone does not show that low-star projects were exposed. Do not inherit a fixed Star interval from another catalog or spend pages on a slice that cannot change the decision.

Keep prior seeds separate from actual query hits. If measuring incremental discovery, freeze a reproducible known set first, stating alias and historical-source limits. “Outside this set” is not “never previously known.”

### Candidate funnel

Raw hits only show that an interface returned an item. Plausible candidates have task-relevant descriptions or documentation. Inspected candidates have enough evidence for their decision-relevant claims. Unread items remain unreviewed, not rejected. After each retrieval batch, briefly scan its returned names/snippets before moving into deep inspection; capture a plausible hit when it might replace a proposed combination, eliminate a major manual step, or overturn a material constraint. A compact working row suffices: `lead/source | possible decision change | check/disposition`. This gate happens when hits are visible, rather than attempting to reconstruct a lost shortlist at the end. It does not require archiving every search result or following every weak lead.

Prioritize candidates by how much of the user's actual route they supply and what material work remains, not by whether one repository contains every step. For a candidate presented as end-to-end, map the required stages to the agent or host, project code, external services, and user. Planning, narration, image generation, rendering, and review can be coordinated across those layers; note setup, missing capabilities, mandatory human work, and handoffs that could break the result. Check that essential host, service, and platform capabilities exist in the user's target environment, not merely in the researcher's current tools. Compare the claimed final artifact with what the project actually produces. Use the map to select what to inspect next, not as a universal checklist for unrelated decisions.

Some repository-search connectors return only names and IDs even when they searched descriptions. A name alone is not enough context to dismiss an otherwise relevant result page. For a consequential broad decision, choose a manageable, task-relevant page and fetch each returned repository's description/topics or its README before treating that page as screened. Batch independent read-only metadata calls where supported. Reduce the page size or refine the query if this would be too costly; preserve the unreviewed tail. Do not silently enrich only the first few names because a project with a generic name can appear later on the same page. Metadata makes a lead plausible, not verified; inspect primary files only for the items that could change the decision.

Sample different approaches and roles where useful: established product, newcomer, specialist, component, and informative historical alternative. There is no fixed candidate count or Star threshold. Retain inactive projects only when they help the decision; label their status. Use IDs for identity where available, but do not collapse distinct subcomponents or useful forks merely because they share an origin.

Reconcile the captured leads before ranking recommendations. Give each material lead an evidence-backed disposition, or mark it deferred and state how it could change the answer. Check whether known omissions were retrieval failures, selection losses, or just unverified candidates; do not invent the reason without evidence.

### Inspection

Deeply read candidates according to uncertainty and decision impact. Normalize comparable inputs, outputs, manual work, dependency branches, limitations, and evidence levels. Do not turn the whole field into a compulsory audit.

For close candidates, make the decisive requirement a small pairwise check: identify whether the behavior comes from the product or a shared browser, indexer, model, parser, or service; compare versions and settings actually shipped by the proposed deployment route. Follow a release change or unresolved issue only when it bears on that requirement or platform. A newer dependency is a reason to test a difference, not proof of better user outcomes. When that evidence cannot separate candidates, explain what the same-sample trial must decide.

If the user names a platform and the candidate's main job depends on a platform-sensitive operation (for example, browser capture, hardware acceleration, filesystem access, or container architecture), use a narrow issue/release query combining that operation with the platform or architecture for the likely choice and strongest challenger. Record whether an issue applies to the proposed image and version or only suggests a test. Do not turn one report from a different host into a product-wide failure claim.

Clone only when local search/history or an authorized reproduction materially helps; use a temporary location and clean disposable data. Reading a project's run commands does not itself authorize executing them.

## Search records and tails

For broad discovery and consequential selection, use the compact [run record](research-record.md) for query receipts, lead dispositions, and route status. Update it while results are visible. The reference explains unknown metadata, failures, collector receipts, and the pre-delivery check; do not reconstruct missing results from the final shortlist.

A full page means truncation risk. Continue when relevant; narrow when noise dominates; partition only on justified ranges. Disclose unexamined tails when the decision budget is better spent on evidence. A child query, a low-star slice, or an author search cannot certify the parent or whole field. Empty/short pages describe the interface response, not the universe. Pages and ranking can change between requests.

Store a compact query summary rather than raw payloads when it suffices. For large retrieval sets, raw count, unique count, inspected count, and dispositions are different quantities. Purposeful samples cannot establish a whole-pool accuracy or recall rate.

## Actions

### Discover

Return a landscape, not just a popularity list.

1. Define the solution forms that could satisfy the user's job.
2. Use diverse query families and record the main coverage boundaries.
3. Group candidates by product form, architecture, user workflow, or another decision-relevant distinction.
4. Select representatives from materially different groups.
5. Explain why shortlisted candidates survived and why plausible alternatives did not.

### Inspect

For one repository, test its fit against the user's constraints and the claims it makes. For comparisons, normalize the same decision-relevant fields across candidates before judging them.

Start with disqualifiers and operational constraints. Do not let a large feature list hide an incompatible license, missing runtime, mandatory cloud service, unclear ownership, or integration burden.

### Verify

Rewrite the request as a falsifiable claim. Define what evidence would support it, what would refute it, and what cannot be concluded from GitHub alone.

Search both directions:

- implementation, tests, shipped Releases, maintainer confirmation, or repeated reports that support the claim;
- contradicting code, closed-as-invalid reports, later fixes, scope limitations, or missing prerequisites that weaken it.

Verdicts are `supported`, `not supported`, or `insufficient evidence`. Qualify the applicable version and time window.

## Tool capability limits

| Surface | Typical route | Important limitation |
|---|---|---|
| Repository metadata, README, Releases | REST, `gh`, raw content | Describes project state and claims, not runtime truth |
| Issues and pull requests | REST, `gh`, browser | Search can duplicate the same root cause; comments may change interpretation |
| Code and configuration | authenticated code search, local clone, raw content | Search coverage and default branch matter |
| Discussions | GraphQL, connected tool, browser | Often unavailable without authentication |
| Historical change | saved snapshots, Releases, commit history | Current metadata alone cannot reconstruct reliable trends |

If a required surface is unavailable, narrow the conclusion and name the missing evidence.

## Stopping conditions

For broad discovery or selection, test the proposed conclusion before stopping:

- For each consequential route, compare the minimum input, the candidate's actual output, and the work still supplied by the user or host. A partial-output tool can be recommended for that partial job, but it cannot close a broader route merely because it accepts the same input. Leave a route open when the decisive transformation is still manual or unsupported.
- Identify a credible alternative or unresolved step that could change the recommendation. Anchor the challenge in the user's constraints or encountered evidence; do not invent an ideal tool or chase every conceivable category. If the existing comparison already addresses it, reuse that evidence.
- Otherwise, make a bounded, targeted query or source check, limited to the question that could change the choice. Record whether it changed the recommendation or remains unresolved. Do not restart the full search, impose a candidate quota, or repeat the check merely to accumulate coverage.
- Account for relevant deferred candidates and open search tails. Decide whether they could still overturn the choice; if so, investigate within scope or present a provisional choice among inspected candidates. Listing the omissions alone does not justify an unrestricted priority claim.
- Separate missing discovery or documentation from untested outcomes. Remaining quality, performance, or cost questions may require execution; this does not prevent resolving an important candidate or configuration question through read-only evidence.

Stop when the evidence supports the requested decision at the stated scope, or when a stated time, access, evidence, or method-validation boundary is reached. No extra search is required for a narrow claim check or when a credible challenge has already been resolved. A method-validation task can finish its agreed checks while domain coverage remains incomplete; explicitly distinguish those outcomes. Do not turn search volume into artificial certainty.
