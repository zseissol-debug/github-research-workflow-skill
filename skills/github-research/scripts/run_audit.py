#!/usr/bin/env python3
"""Check a bounded research record; never certify source truth or field-wide recall."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def empty_record(question: str) -> dict[str, Any]:
    return {
        "schema_version": 1, "question": question,
        "searches": [], "leads": [], "routes": [],
        "conclusion": {"scope": "", "recommended_leads": [], "limitations": [], "stop_reason": ""},
    }


def audit(run: dict[str, Any]) -> dict[str, Any]:
    """Report missing accounting separately from honestly bounded evidence."""
    problems: list[str] = []
    limits: list[str] = []
    unresolved: list[str] = []
    route_gaps: list[str] = []

    def text(value: Any) -> bool:
        return isinstance(value, str) and bool(value.strip())

    def strings(value: Any) -> bool:
        return isinstance(value, list) and all(text(item) for item in value)

    def objects(field: str) -> dict[str, dict[str, Any]]:
        entries = run.get(field)
        if not isinstance(entries, list):
            problems.append(f"{field}: expected a list")
            return {}
        indexed = {}
        for item in entries:
            if not isinstance(item, dict) or not text(item.get("id")):
                problems.append(f"{field}: each entry needs a nonempty id")
            elif item["id"] in indexed:
                problems.append(f"{field}: duplicate id {item['id']}")
            else:
                indexed[item["id"]] = item
        return indexed

    def require_text(item: dict, fields: tuple[str, ...], where: str) -> None:
        for field in fields:
            if not text(item.get(field)):
                problems.append(f"{where}.{field}: required text")

    def timestamp(value: Any, where: str) -> None:
        try:
            stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                raise ValueError("missing timezone")
        except (AttributeError, TypeError, ValueError):
            problems.append(f"{where}: expected an ISO timestamp with timezone")

    def refs(item: dict, field: str, targets: dict, where: str) -> list[str]:
        value = item.get(field)
        if not strings(value):
            problems.append(f"{where}.{field}: expected a list of ids")
            return []
        for ref in value:
            if ref not in targets:
                problems.append(f"{where}.{field}: unknown id {ref}")
        return value

    if not isinstance(run, dict):
        raise ValueError("run must be an object")
    if type(run.get("schema_version")) is not int or run["schema_version"] != 1:
        problems.append("schema_version: expected 1")
    require_text(run, ("question",), "run")
    searches, leads, routes = (objects(field) for field in ("searches", "leads", "routes"))
    if not searches:
        problems.append("searches: no retrieval record; missing evidence is not an empty successful search")
    if not routes:
        problems.append("routes: record the consequential input-to-output routes before claiming coverage")

    for sid, search in searches.items():
        where = f"searches.{sid}"
        require_text(search, ("query", "surface", "trigger", "next_action"), where)
        if not strings(search.get("hit_ids")):
            problems.append(f"{where}.hit_ids: expected captured hit ids (not necessarily every raw hit)")
        if search.get("screening") not in ("complete", "partial", "not_screened"):
            problems.append(f"{where}.screening: expected complete, partial, or not_screened")
        elif search["screening"] != "complete":
            limits.append(f"{sid}: returned batch not fully screened")
        if search.get("tail") not in ("exhausted", "open", "unknown"):
            problems.append(f"{where}.tail: expected exhausted, open, or unknown")
        elif search["tail"] != "exhausted":
            limits.append(f"{sid}: search tail {search['tail']}; {search.get('next_action', '')}")
        attempts = search.get("requests")
        if not isinstance(attempts, list) or not attempts:
            problems.append(f"{where}.requests: no actual request receipts")
            continue
        valid = []
        for i, attempt in enumerate(attempts):
            loc = f"{where}.requests[{i}]"
            if not isinstance(attempt, dict):
                problems.append(f"{loc}: expected an object")
                continue
            before = len(problems)
            if "at" in attempt and attempt["at"] is None:
                timestamp(attempt.get("recorded_at"), f"{loc}.recorded_at")
                require_text(attempt, ("time_note",), loc)
                limits.append(f"{sid}: request time not captured; {attempt.get('time_note', '')}")
            else:
                timestamp(attempt.get("at"), f"{loc}.at")
            if not isinstance(attempt.get("params"), dict):
                problems.append(f"{loc}.params: record actual parameters, including pagination when available")
            else:
                for field in ("page", "per_page"):
                    if field in attempt["params"] and (type(attempt["params"][field]) is not int or attempt["params"][field] < 1):
                        problems.append(f"{loc}.params.{field}: expected a positive integer")
                if "q" in attempt["params"] and attempt["params"]["q"] != search.get("query"):
                    problems.append(f"{loc}.params.q: differs from the recorded query")
            for field in ("returned_count", "total_count"):
                value = attempt.get(field)
                if field not in attempt or (value is not None and (type(value) is not int or value < 0)):
                    problems.append(f"{loc}.{field}: expected a nonnegative integer or explicit null")
            for field in ("incomplete_results", "has_next"):
                if field not in attempt or (attempt[field] is not None and type(attempt[field]) is not bool):
                    problems.append(f"{loc}.{field}: expected boolean or explicit null")
            if attempt.get("status") == "error":
                require_text(attempt, ("error",), loc)
                if attempt.get("returned_count") is not None:
                    problems.append(f"{loc}: a failed request needs returned_count=null, not zero")
                limits.append(f"{sid}: retrieval failed; {attempt.get('error', '')}")
            elif attempt.get("status") == "success":
                if attempt.get("error") is not None:
                    problems.append(f"{loc}: success cannot carry an error")
                if attempt.get("incomplete_results") is True:
                    limits.append(f"{sid}: provider reported incomplete results")
            else:
                problems.append(f"{loc}.status: expected success or error")
            if len(problems) == before:
                valid.append(attempt)
        if len(valid) != len(attempts):
            continue
        if search.get("hit_ids") and not any(a["status"] == "success" for a in valid):
            problems.append(f"{where}: hits cannot come from only failed requests")
        successful = [a for a in valid if a["status"] == "success"]
        if search.get("hit_ids") and successful and all(a["returned_count"] == 0 for a in successful):
            problems.append(f"{where}: captured hits contradict the successful zero-result receipts")
        # A short page or explicit provider boundary concerns this query, never the field.
        last = valid[-1]
        numbered = [a["params"].get("page") for a in successful]
        numbered_sequence = bool(numbered) and numbered == list(range(1, len(numbered) + 1))
        continuous = len(successful) <= 1 if all(n is None for n in numbered) else numbered_sequence
        same_request = all(
            {k: v for k, v in a["params"].items() if k != "page"} ==
            {k: v for k, v in last["params"].items() if k != "page"}
            for a in successful
        )
        count, per_page = last["returned_count"], last["params"].get("per_page")
        short = type(count) is int and type(per_page) is int and 0 <= count < per_page
        totals = [a["total_count"] for a in valid]
        counts = [a["returned_count"] for a in valid]
        total_seen = continuous and bool(totals) and all(type(n) is int for n in counts) and type(totals[-1]) is int and sum(counts) >= totals[-1]
        known_open = (not continuous or not same_request or last["has_next"] is True or
                      any(a["status"] == "error" or a["incomplete_results"] is True for a in valid))
        if type(totals[-1]) is int and all(type(n) is int for n in counts) and sum(counts) < totals[-1]:
            known_open = True
        if search.get("tail") == "exhausted" and (known_open or not (short or total_seen or last["has_next"] is False)):
            problems.append(f"{where}.tail: exhaustion is not supported by the recorded responses")

    for lid, lead in leads.items():
        where = f"leads.{lid}"
        require_text(lead, ("source", "impact"), where)
        query_ids = refs(lead, "query_ids", searches, where)
        if lead.get("origin") == "query":
            if not query_ids:
                problems.append(f"{where}: query-origin lead needs its actual query id")
            elif not any(lid in searches[q].get("hit_ids", []) for q in query_ids if q in searches and isinstance(searches[q].get("hit_ids"), list)):
                problems.append(f"{where}: not present in the cited query's captured hits")
        elif lead.get("origin") != "prior":
            problems.append(f"{where}.origin: expected prior or query")
        status = lead.get("status")
        if status not in ("pending", "inspected", "excluded", "deferred", "insufficient_evidence"):
            problems.append(f"{where}.status: invalid disposition")
        elif status == "pending":
            problems.append(f"{where}: decision-changing lead has no disposition")
        else:
            require_text(lead, ("reason",), where)
        evidence = lead.get("evidence")
        if not strings(evidence):
            problems.append(f"{where}.evidence: expected source pointers")
        elif status in ("inspected", "excluded") and not evidence:
            problems.append(f"{where}: {status} needs supporting evidence")
        if status in ("deferred", "insufficient_evidence", "pending"):
            unresolved.append(lid)
            limits.append(f"{lid}: unresolved decision-changing lead ({status})")

    for rid, route in routes.items():
        where = f"routes.{rid}"
        require_text(route, ("input", "output", "reason"), where)
        lead_ids = refs(route, "lead_ids", leads, where)
        status = route.get("status")
        if status not in ("covered", "partial", "open", "out_of_scope"):
            problems.append(f"{where}.status: invalid route status")
        if not strings(route.get("evidence")):
            problems.append(f"{where}.evidence: expected source pointers")
        if status == "covered":
            if not route.get("evidence") or not any(leads[l].get("status") == "inspected" for l in lead_ids if l in leads):
                problems.append(f"{where}: covered route needs an inspected candidate and output evidence")
        if status in ("partial", "open"):
            route_gaps.append(rid)
            limits.append(f"{rid}: input-to-output route {status}; {route.get('reason', '')}")

    conclusion = run.get("conclusion")
    if not isinstance(conclusion, dict):
        problems.append("conclusion: expected an object")
    else:
        require_text(conclusion, ("scope", "stop_reason"), "conclusion")
        recommended = refs(conclusion, "recommended_leads", leads, "conclusion")
        for lid in recommended:
            if lid in leads and leads[lid].get("status") != "inspected":
                problems.append(f"conclusion: recommendation {lid} has not been inspected")
        if not strings(conclusion.get("limitations")):
            problems.append("conclusion.limitations: expected a list of explicit bounds")
    if not any(l.get("status") == "inspected" for l in leads.values()):
        limits.append("No inspected candidate evidence; a completed empty search is not a field-wide negative finding")
    if limits and isinstance(conclusion, dict) and not conclusion.get("limitations"):
        problems.append("conclusion.limitations: unresolved findings must bound the answer")
    return {
        "record_status": "needs_work" if problems else "bounded" if limits else "consistent",
        "record_issues": problems,
        "unresolved_leads": unresolved,
        "route_gaps": route_gaps,
        "limits": list(dict.fromkeys(limits)),
        "counts": {"searches": len(searches), "leads": len(leads), "routes": len(routes)},
        "scope_note": "Checks only this supplied record. Consistent is not selection approval, source verification, runtime validation, or field-wide recall.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="create an empty record without overwriting an existing file")
    init.add_argument("path", type=Path)
    init.add_argument("--question", required=True)
    check = sub.add_parser("check", help="check records; 0=consistent/bounded, 1=needs work, 2=invalid input")
    check.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "init":
            with args.path.open("x", encoding="utf-8") as stream:
                json.dump(empty_record(args.question), stream, ensure_ascii=False, indent=2)
                stream.write("\n")
            return 0
        result = audit(json.loads(args.path.read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result["record_status"] == "needs_work" else 0
    except (OSError, ValueError) as exc:
        print(f"run_audit: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
