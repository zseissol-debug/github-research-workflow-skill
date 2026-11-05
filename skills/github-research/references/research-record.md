# A checkable research run

Use this record for broad discovery and consequential multi-candidate selection. A narrow repository read or claim check does not need it. Keep one compact `research-run.json` beside the task's output, outside the installed Skill. Update it while evidence is visible, not from memory after writing the answer. Existing project records may be used if they preserve the same information; convert them without inventing missing observations before running the checker.

```bash
python3 <skill-directory>/scripts/run_audit.py init research-run.json --question 'The actual research question'
```

Initialization creates an intentionally incomplete record and refuses to overwrite a file. Missing provider metadata is `null`; a failed request is not a successful zero-hit query. Do not store tokens, cookies, authorization headers, or unrelated user data.

## Record structure

This is a **synthetic format example**, not research evidence:

```json
{
  "schema_version": 1,
  "question": "Which tool turns a folder of documents into a local searchable archive?",
  "searches": [{
    "id": "q1",
    "query": "local document archive",
    "surface": "repository metadata search",
    "trigger": "Find products that supply both storage and retrieval",
    "requests": [{
      "at": "2026-10-12T00:00:00Z",
      "params": {"q": "local document archive", "page": 1, "per_page": 10},
      "status": "success",
      "returned_count": 1,
      "total_count": 1,
      "incomplete_results": false,
      "has_next": false,
      "error": null
    }],
    "hit_ids": ["example/archive"],
    "screening": "complete",
    "tail": "exhausted",
    "next_action": "Read the import and search implementation"
  }],
  "leads": [{
    "id": "example/archive",
    "origin": "query",
    "source": "q1 metadata result",
    "query_ids": ["q1"],
    "impact": "Might remove a separate indexing step",
    "status": "inspected",
    "reason": "Import and retrieval documented; runtime quality remains untested",
    "evidence": ["https://example.org/archive/import-and-search"]
  }],
  "routes": [{
    "id": "documents-to-search",
    "input": "An existing folder of documents",
    "output": "Persistent local content with searchable full text",
    "status": "covered",
    "lead_ids": ["example/archive"],
    "reason": "The inspected implementation connects import to the search index",
    "evidence": ["https://example.org/archive/import-and-search"]
  }],
  "conclusion": {
    "scope": "A bounded static comparison for this input and output",
    "recommended_leads": ["example/archive"],
    "limitations": ["No independent runtime trial; the query does not cover the whole field"],
    "stop_reason": "The requested initial comparison is supported at this scope"
  }
}
```

## Search receipts

Use a separate search entry for each query/sort/filter combination. `requests` contains its actual pages or attempts, preserving successful pages if a later one fails. Put real tool arguments in `params`; do not invent pagination for a web tool that does not expose it. `at` is the request time with a timezone. Capture it when making the request. If it was not captured, use `at: null`, the actual later `recorded_at` timestamp, and a `time_note` explaining the missing observation and any known interval; this remains a recorded limit. Never substitute the time of writing the report for the request time. Counts and provider flags are integers/booleans or explicit `null`. A request with `status: error` needs its error and `returned_count: null`.

The optional collector's `data.searches[]` supplies `query`, `surface`, and `requests`, plus outcome and stopping metadata. Copy those receipts and add `id`, `trigger`, `hit_ids`, `screening`, `tail`, and `next_action`. Extra collector fields may remain. Search commands preserve successful results after later failures: exit 0 means successful requests, 1 partial retrieval, 2 failed retrieval. Retain emitted JSON on a nonzero exit. Other commands retain their existing behavior.

For connectors or web search, record receipts directly from tool results. `hit_ids` captures identities needed to trace important leads; it need not contain every raw hit. Only use `screening: complete` after checking the visible batch's descriptions/snippets, including metadata enrichment for names-only results. Otherwise use `partial` or `not_screened` and describe remaining work in `next_action`.

`tail` is `exhausted`, `open`, or `unknown`. Exhaustion describes only this query's observed boundary. A full page, remaining total, incomplete flag, paging gap, or failure cannot be silently closed. A narrower query does not exhaust its parent. An unknown web result window stays unknown. This does not require infinite pagination: disclose the boundary and constrain the conclusion.

The checker can verify consecutive numbered pages; it cannot establish cursor traversal from counts alone. For multiple unnumbered requests, keep the tail `unknown` and explain any independently checked cursor traversal in `next_action`. Repeated requests never add coverage merely by adding their counts.

## Leads and routes

Capture leads that could change the choice, manual work, or output; state that possible change in `impact`. IDs may identify repositories, products, components, or workflows. Keep meaningful forks separate. A query-origin lead references its actual `query_ids` and appears in a cited query's `hit_ids`. Linked-source or author expansion counts as a query/read with its real URL and parameters. Prior user/project leads use `origin: prior`, a provenance pointer in `source`, and may have empty `query_ids`.

Lead `status` is `pending`, `inspected`, `excluded`, `deferred`, or `insufficient_evidence`. The last four need a reason. Inspection and exclusion need source pointers in `evidence`; local pointers resolve relative to the record. Deferred and insufficient-evidence leads remain decision limits even though they have dispositions. Do not exclude them just to clear the check. The checker does not open or verify sources.

Routes describe consequential **input → actual output**, with status `covered`, `partial`, `open`, or `out_of_scope`. A covered route links inspected candidates and output evidence. Input acceptance, a field, or a template alone does not prove the transformation. State missing user/host work in `reason`. Excluding a route requires a reason tied to user scope, not lack of search results. This is a task-specific map, not a prescribed taxonomy.

## Before delivery

```bash
python3 <skill-directory>/scripts/run_audit.py check research-run.json
```

Read the output, not just the exit code:

- `needs_work` (exit 1): missing receipts, pending important leads, unsupported closure, invalid references, or a conclusion omitting recorded limits. Repair the record or retrieve evidence; never fabricate it. If access/time prevents repair, deliver an explicitly incomplete result and name what could not be established.
- `bounded` (exit 0): the record is usable, but deferred leads, open routes, tails, failures, or lack of inspected candidates constrain it. Resolve a limit when it could change the decision and fits the task; otherwise carry specific limits into the answer and restrict rankings to inspected candidates.
- `consistent` (exit 0): no such accounting issue was detected. This is **not** recommendation approval, source verification, runtime validation, saturation, or proof against unknown omissions.

Compare the final prose with the actual remaining leads/routes/tails. `limitations` must name consequential bounds, not just a generic disclaimer. The script checks presence and consistency, not semantic honesty or completeness. A completed zero-hit search cannot establish that no suitable project exists.

For a maintained project inventory, [research-memory.md](research-memory.md)'s `lead_audit.py` additionally detects known-lead identity and retrieval/selection gaps. Its `actionable_gap: false` only means supplied relevant leads have dispositions; it does not replace this run check.
