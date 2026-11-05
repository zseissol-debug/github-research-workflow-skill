#!/usr/bin/env python3
"""Check a project-owned GitHub lead inventory and a bounded research run.

This script does not search GitHub or judge whether a project is suitable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DISPOSITIONS = {"inspected", "excluded", "deferred", "insufficient_evidence"}


def repo_key(value: str) -> str:
    """Normalize a repository name or root GitHub URL without merging forks."""
    if value.startswith("https://github.com/"):
        value = value.removeprefix("https://github.com/").rstrip("/")
        value = value.removesuffix(".git")
    if not REPO_RE.fullmatch(value):
        raise ValueError(f"expected owner/name or a root GitHub URL, got {value!r}")
    return value.casefold()


def load_inventory(path: Path) -> tuple[list[dict[str, Any]], dict[str, str]]:
    leads: list[dict[str, Any]] = []
    aliases: dict[str, str] = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            lead = json.loads(line)
            if not isinstance(lead, dict):
                raise ValueError("line must be an object")
            repo = repo_key(lead["repo"])
            sources = lead["sources"]
            if not isinstance(sources, list) or not sources:
                raise ValueError("sources must be a nonempty list")
            for source in sources:
                if not isinstance(source, dict) or not all(
                    isinstance(source.get(field), str) and source[field]
                    for field in ("kind", "url", "observed_at")
                ):
                    raise ValueError("each source needs kind, url, observed_at")
                if not DATE_RE.fullmatch(source["observed_at"]):
                    raise ValueError("source observed_at must be YYYY-MM-DD")
                try:
                    date.fromisoformat(source["observed_at"])
                except ValueError as exc:
                    raise ValueError("source observed_at must be a real date") from exc
            if lead.get("status") not in {"catalog_lead", "static_inspected"}:
                raise ValueError("status must be catalog_lead or static_inspected")
            names = [repo, *[repo_key(name) for name in lead.get("aliases", [])]]
            for name in names:
                if name in aliases:
                    raise ValueError(f"duplicate repository or alias {name!r}")
                aliases[name] = repo
            leads.append(lead)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise ValueError(f"{path}:{number}: {exc}") from exc
    return leads, aliases


def canonical(value: str, aliases: dict[str, str]) -> str:
    key = repo_key(value)
    return aliases.get(key, key)


def load_run(path: Path, aliases: dict[str, str]) -> dict[str, Any]:
    run = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(run, dict):
        raise ValueError("run must be an object")
    for field in ("relevant_known", "search_hits", "plausible_hits"):
        if field not in run:
            raise ValueError(f"run missing required field: {field}")
        if not isinstance(run[field], list):
            raise ValueError(f"{field} must be a list")
    if "dispositions" not in run:
        raise ValueError("run missing required field: dispositions")
    if "claimed_new_to_project" in run and not isinstance(run["claimed_new_to_project"], list):
        raise ValueError("claimed_new_to_project must be a list")
    if not isinstance(run["dispositions"], dict):
        raise ValueError("dispositions must be an object")
    dispositions: dict[str, dict[str, str]] = {}
    for raw_name, disposition in run["dispositions"].items():
        key = canonical(raw_name, aliases)
        if key in dispositions:
            raise ValueError(f"duplicate disposition for {key}")
        if not isinstance(disposition, dict) or disposition.get("status") not in DISPOSITIONS:
            raise ValueError(f"invalid disposition for {raw_name}")
        if not isinstance(disposition.get("reason"), str) or not disposition["reason"].strip():
            raise ValueError(f"disposition for {raw_name} needs a reason")
        dispositions[key] = disposition
    normalized = {
        "relevant_known": {canonical(item, aliases) for item in run["relevant_known"]},
        "search_hits": {canonical(item, aliases) for item in run["search_hits"]},
        "plausible_hits": {canonical(item, aliases) for item in run["plausible_hits"]},
        "claimed_new_to_project": {canonical(item, aliases) for item in run.get("claimed_new_to_project", [])},
        "dispositions": dispositions,
    }
    if normalized["plausible_hits"] - normalized["search_hits"]:
        raise ValueError("plausible_hits must be drawn from this run's search_hits")
    return normalized


def audit(inventory: dict[str, str], run: dict[str, Any]) -> dict[str, Any]:
    unknown = sorted(run["relevant_known"] - set(inventory.values()))
    if unknown:
        raise ValueError(f"relevant_known absent from inventory: {', '.join(unknown)}")
    known = run["relevant_known"]
    hits = run["search_hits"]
    handled = set(run["dispositions"])
    output = {
        "known_retrieved_and_handled": sorted(known & hits & handled),
        "known_handled_from_prior_lead_only": sorted((known - hits) & handled),
        "known_retrieved_but_unhandled": sorted((known & hits) - handled),
        "known_neither_retrieved_nor_handled": sorted(known - hits - handled),
        "other_plausible_hits_unhandled": sorted(run["plausible_hits"] - handled - known),
        "claimed_new_but_in_inventory": sorted(run["claimed_new_to_project"] & set(inventory.values())),
        "retrieval_gap_among_known": sorted(known - hits),
        "scope_note": "Only explicitly marked relevant known leads and plausible hits are audited; this is not field-wide recall.",
    }
    output["actionable_gap"] = any(
        output[field]
        for field in (
            "known_retrieved_but_unhandled",
            "known_neither_retrieved_nor_handled",
            "other_plausible_hits_unhandled",
            "claimed_new_but_in_inventory",
        )
    )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path, help="project-owned JSONL lead inventory")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    finder = sub.add_parser("find", help="literal case-insensitive lead lookup")
    finder.add_argument("term")
    finder.add_argument("--limit", type=int, default=20)
    auditor = sub.add_parser("audit", help="classify a bounded run's known-lead gaps")
    auditor.add_argument("run", type=Path)
    args = parser.parse_args()
    try:
        leads, aliases = load_inventory(args.inventory)
        if args.command == "validate":
            print(json.dumps({"valid": True, "leads": len(leads), "aliases": len(aliases) - len(leads)}))
        elif args.command == "find":
            if args.limit < 1:
                raise ValueError("--limit must be positive")
            term = args.term.casefold()
            found = [
                lead for lead in leads
                if term in " ".join(str(lead.get(field, "")) for field in ("repo", "description", "kind", "terms")).casefold()
            ]
            print(json.dumps({"matching": len(found), "shown": min(len(found), args.limit), "truncated": len(found) > args.limit, "leads": found[:args.limit]}, ensure_ascii=False))
        else:
            print(json.dumps(audit(aliases, load_run(args.run, aliases)), ensure_ascii=False, indent=2))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"lead_audit: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
