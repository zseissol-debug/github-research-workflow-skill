# Reusing research leads across tasks

Use this only when the user supplies prior notes/catalogs or the active project already maintains research leads. A one-off narrow verification does not need an inventory. Never search a user's entire filesystem for one; use the current project or an explicitly supplied location. Treat saved descriptions and labels as dated leads, not as current proof.

## Carry forward and expand

At the beginning, select prior leads whose **input-to-output route** could affect this task. Keep their original source and observation date, and freeze the relevant set before new search if measuring rediscovery. A project already inspected in another context may still need rechecking for the current input, version and constraints. A catalog entry with no primary-source inspection remains `catalog_lead`.

Extract useful vocabulary from those leads: the project's own task names, underlying framework/protocol, dependent tools, adjacent workflow, author, and named alternatives. Turn one of these into a follow-up search only to resolve a route or decision gap; record the trigger and actual query. An author expansion is for a relevant creator's other work, not a fixed author whitelist. If search ranking hides newer or low-star routes, use a justified query or non-overlapping partition and record returned pages/tail; no universal Star ranges are required.

After retrieval, reconcile: (a) known relevant lead absent from query hits; (b) visible promising hit lost before disposition; (c) inspected and excluded/deferred with a reason; (d) current source genuinely changes a prior judgment. A prior lead can be inspected without being rediscovered; report it as a prior lead rather than a novel result. Do not claim full recall from the number of saved leads or a successful canary.

## Optional project-owned JSONL inventory

Keep the inventory alongside project reports, not inside this installed Skill. Each line is one repository; distinct forks stay separate. The minimal record is:

```json
{"repo":"owner/name","description":"source's dated description","kind":"free-form route label","terms":["task term","framework"],"status":"catalog_lead","sources":[{"kind":"catalog","url":"https://example.org/list","observed_at":"2026-10-07"}]}
```

`status` is `catalog_lead` or `static_inspected`; neither means runtime validation. Add `aliases` only for a verified rename or equivalent root URL, not for a distinct fork. A record can retain multiple dated sources. A current primary-source check belongs in the research report with its version and evidence level; update the inventory's status and sources only when the project workflow calls for durable records. Avoid overwriting user-maintained files without authorization.

For local archived evidence, `sources[].url` may use a project-relative identifier such as `project:reports/old-search.md`; resolve it against that project's documented root. It is a provenance pointer, not a web URL or proof that the target still exists.

The optional standard-library checker, `python3 <skill-directory>/scripts/lead_audit.py INVENTORY validate`, checks repository identity/aliases, required source fields, and a valid `YYYY-MM-DD` observation date. It does not open source pointers or verify their truth. `find TERM` performs literal lookup and reports truncation, not semantic relevance. For consequential ongoing work, a small run record can be checked with `audit RUN.json`:

```json
{"relevant_known":["owner/name"],"search_hits":[],"plausible_hits":[],"dispositions":{"owner/name":{"status":"inspected","reason":"Checked current input/output path in the primary docs."}}}
```

`relevant_known` is selected from the inventory **before** evaluating the run, not a hindsight list of whatever the final answer named. `search_hits` records this run's actual returned repositories; prior leads do not count as search hits. `plausible_hits` contains current visible hits judged potentially decision-changing before deep inspection. `dispositions` uses `inspected`, `excluded`, `deferred`, or `insufficient_evidence`, each with a concrete reason. The checker distinguishes a prior-only lead, a query miss, and a selection loss. It cannot detect relevant projects absent from both memory and search, assess source truth, or establish a field-wide recall rate. Use its output to target a query or source check, not to force an irrelevant project into the recommendation.

All four fields are required, including an explicit `search_hits: []` when a completed search returned none. If retrieval failed or its output was not recorded, disclose that failure and do not turn missing hits into an empty successful result. The checker rejects a missing field, but it cannot independently verify that a supplied empty array represents a completed search.

If a report claims repositories are *new to this project*, include them as `claimed_new_to_project` in the run record. The checker flags any already present in the inventory, including verified rename aliases. “Newly returned by this query” is a different claim and needs no such field. An incomplete inventory still cannot prove an absent project was never known elsewhere in the project.

`actionable_gap: false` means only that the supplied relevant leads have dispositions and no checked identity conflict. An empty record or a deferred lead can produce that result. For broad discovery or consequential selection, also use [research-record.md](research-record.md) to account for actual retrieval, unresolved leads, and input-to-output gaps before delivering the answer.
