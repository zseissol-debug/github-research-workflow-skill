#!/usr/bin/env python3
"""Small, read-only GitHub REST collector for the github-research skill."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import http.client
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


API_ROOT = "https://api.github.com"
USER_AGENT = "codex-github-research-skill/1.0"


class GitHubError(RuntimeError):
    pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def token() -> str | None:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def request(
    path: str,
    params: dict[str, Any] | None = None,
    accept: str | None = None,
) -> tuple[Any, dict[str, str]]:
    query = urllib.parse.urlencode(
        {key: value for key, value in (params or {}).items() if value is not None}
    )
    url = f"{API_ROOT}{path}"
    if query:
        url = f"{url}?{query}"

    headers = {
        "Accept": accept or "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    auth_token = token()
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read()
            response_headers = {key.lower(): value for key, value in response.headers.items()}
            content_type = response_headers.get("content-type", "")
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except (OSError, http.client.HTTPException) as body_error:
            raise GitHubError(f"GitHub API returned HTTP {exc.code}; error body could not be read: {body_error}") from body_error
        try:
            parsed = json.loads(detail)
            message = parsed.get("message", detail)
        except json.JSONDecodeError:
            message = detail
        raise GitHubError(f"GitHub API returned HTTP {exc.code}: {message}") from exc
    except (OSError, http.client.HTTPException) as exc:
        raise GitHubError(f"Could not reach GitHub API: {getattr(exc, 'reason', str(exc))}") from exc

    if accept and "raw" in accept:
        return raw.decode("utf-8", errors="replace"), response_headers
    if "json" in content_type:
        return json.loads(raw.decode("utf-8")), response_headers
    return raw.decode("utf-8", errors="replace"), response_headers


def repo_path(repo: str, suffix: str = "") -> str:
    if repo.count("/") != 1 or any(not part for part in repo.split("/")):
        raise GitHubError("Repository must be written as owner/name")
    safe_repo = urllib.parse.quote(repo, safe="/")
    return f"/repos/{safe_repo}{suffix}"


def paged(
    path: str,
    params: dict[str, Any],
    pages: int,
) -> tuple[list[Any], dict[str, str]]:
    output: list[Any] = []
    last_headers: dict[str, str] = {}
    for page in range(1, pages + 1):
        page_params = dict(params)
        page_params["page"] = page
        data, last_headers = request(path, page_params)
        if not isinstance(data, list):
            raise GitHubError("Expected a list response from GitHub")
        output.extend(data)
        if len(data) < int(params.get("per_page", 30)):
            break
    return output, last_headers


def search(
    path: str,
    query: str,
    sort: str | None,
    order: str,
    per_page: int,
    pages: int,
) -> tuple[dict[str, Any], dict[str, str]]:
    items: list[Any] = []
    total_count: int | None = None
    requests: list[dict[str, Any]] = []
    stop_reason = "page_budget"
    last_headers: dict[str, str] = {}
    for page in range(1, pages + 1):
        params = {"q": query, "order": order, "per_page": per_page, "page": page}
        if sort is not None:
            params["sort"] = sort
        receipt = {
            "at": utc_now(), "params": params, "status": "error",
            "returned_count": None, "total_count": None,
            "incomplete_results": None, "has_next": None, "error": None,
        }
        requests.append(receipt)
        try:
            data, last_headers = request(path, params)
            if not isinstance(data, dict) or not isinstance(data.get("items"), list):
                raise GitHubError("Expected a search response from GitHub")
            if not all(isinstance(item, dict) for item in data["items"]):
                raise GitHubError("Expected search items to be objects")
            total = data.get("total_count")
            if total is not None and (type(total) is not int or total < 0):
                raise GitHubError("Expected total_count to be a nonnegative integer or null")
            incomplete_value = data.get("incomplete_results")
            if incomplete_value is not None and type(incomplete_value) is not bool:
                raise GitHubError("Expected incomplete_results to be boolean or null")
        except (GitHubError, json.JSONDecodeError) as exc:
            receipt["error"] = str(exc)
            stop_reason = "request_error"
            break
        total_count = data.get("total_count")
        page_items = data["items"]
        receipt.update({
            "status": "success", "returned_count": len(page_items),
            "total_count": total_count,
            "incomplete_results": data.get("incomplete_results"),
            "has_next": 'rel="next"' in last_headers["link"] if "link" in last_headers else None,
        })
        items.extend(page_items)
        if len(page_items) < per_page:
            stop_reason = "short_page"
            break
        if receipt["has_next"] is False or (total_count is not None and page * per_page >= total_count):
            stop_reason = "reported_end"
            break
    completed = sum(r["status"] == "success" for r in requests)
    incomplete_values = [r["incomplete_results"] for r in requests if r["status"] == "success"]
    incomplete = (True if True in incomplete_values else
                  False if incomplete_values and all(v is False for v in incomplete_values) else None)
    return {
        "query": query,
        "surface": f"GitHub REST {path}",
        "page_budget": pages,
        "requests": requests,
        "outcome": "success" if completed == len(requests) else "partial" if completed else "error",
        "stop_reason": stop_reason,
        "total_count": total_count,
        "incomplete_results": incomplete,
        "items": items,
    }, last_headers


def search_many(
    path: str,
    queries: list[str],
    sort: str | None,
    order: str,
    per_page: int,
    pages: int,
) -> tuple[dict[str, Any], dict[str, str]]:
    unique: dict[str, dict[str, Any]] = {}
    total_count_by_query: dict[str, int | None] = {}
    searches: list[dict[str, Any]] = []
    fetched_items = 0
    last_headers: dict[str, str] = {}

    for query in queries:
        result, last_headers = search(path, query, sort, order, per_page, pages)
        searches.append({key: value for key, value in result.items() if key != "items"})
        total_count_by_query[query] = result["total_count"]
        fetched_items += len(result["items"])
        for item in result["items"]:
            key = str(
                item.get("node_id")
                or item.get("html_url")
                or item.get("full_name")
                or item.get("id")
            )
            if key not in unique:
                unique[key] = {**item, "matched_queries": [query]}
            else:
                if query not in unique[key]["matched_queries"]:
                    unique[key]["matched_queries"].append(query)

    outcomes = [entry["outcome"] for entry in searches]
    incomplete_values = [entry["incomplete_results"] for entry in searches]
    return {
        "queries": queries,
        "searches": searches,
        "outcome": "success" if all(v == "success" for v in outcomes) else "error" if all(v == "error" for v in outcomes) else "partial",
        "total_count_by_query": total_count_by_query,
        "incomplete_results": (True if True in incomplete_values else False if all(v is False for v in incomplete_values) else None),
        "fetched_items": fetched_items,
        "unique_items": len(unique),
        "duplicates_removed": fetched_items - len(unique),
        "items": list(unique.values()),
    }, last_headers


def cut(value: Any, limit: int = 1500) -> Any:
    if not isinstance(value, str) or len(value) <= limit:
        return value
    return f"{value[:limit]}\n...[truncated by github_collect.py]"


def actor(value: Any) -> str | None:
    return value.get("login") if isinstance(value, dict) else None


def license_id(value: Any) -> str | None:
    return value.get("spdx_id") if isinstance(value, dict) else None


def labels(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.get("name") for item in value if isinstance(item, dict) and item.get("name")]


def summarize_item(command: str, item: dict[str, Any]) -> dict[str, Any]:
    matched = item.get("matched_queries")
    if command == "search-repos":
        result = {
            "full_name": item.get("full_name"),
            "html_url": item.get("html_url"),
            "description": item.get("description"),
            "fork": item.get("fork"),
            "archived": item.get("archived"),
            "created_at": item.get("created_at"),
            "updated_at": item.get("updated_at"),
            "pushed_at": item.get("pushed_at"),
            "stargazers_count": item.get("stargazers_count"),
            "forks_count": item.get("forks_count"),
            "open_issues_count": item.get("open_issues_count"),
            "language": item.get("language"),
            "license": license_id(item.get("license")),
            "topics": item.get("topics", []),
            "default_branch": item.get("default_branch"),
            "size": item.get("size"),
            "owner_type": (item.get("owner") or {}).get("type"),
        }
    elif command in {"search-issues", "issues"}:
        result = {
            "type": "pull_request" if "pull_request" in item else "issue",
            "repository_url": item.get("repository_url"),
            "number": item.get("number"),
            "title": item.get("title"),
            "html_url": item.get("html_url"),
            "state": item.get("state"),
            "state_reason": item.get("state_reason"),
            "user": actor(item.get("user")),
            "author_association": item.get("author_association"),
            "labels": labels(item.get("labels")),
            "comments": item.get("comments"),
            "created_at": item.get("created_at"),
            "updated_at": item.get("updated_at"),
            "closed_at": item.get("closed_at"),
            "body": cut(item.get("body")),
        }
    elif command == "search-code":
        result = {
            "repository": (item.get("repository") or {}).get("full_name"),
            "name": item.get("name"),
            "path": item.get("path"),
            "sha": item.get("sha"),
            "html_url": item.get("html_url"),
            "score": item.get("score"),
        }
    elif command == "pulls":
        result = {
            "number": item.get("number"),
            "title": item.get("title"),
            "html_url": item.get("html_url"),
            "state": item.get("state"),
            "draft": item.get("draft"),
            "user": actor(item.get("user")),
            "author_association": item.get("author_association"),
            "created_at": item.get("created_at"),
            "updated_at": item.get("updated_at"),
            "closed_at": item.get("closed_at"),
            "merged_at": item.get("merged_at"),
            "base": (item.get("base") or {}).get("ref"),
            "head": (item.get("head") or {}).get("ref"),
            "labels": labels(item.get("labels")),
            "body": cut(item.get("body")),
        }
    elif command == "releases":
        result = {
            "tag_name": item.get("tag_name"),
            "name": item.get("name"),
            "html_url": item.get("html_url"),
            "draft": item.get("draft"),
            "prerelease": item.get("prerelease"),
            "author": actor(item.get("author")),
            "created_at": item.get("created_at"),
            "published_at": item.get("published_at"),
            "body": cut(item.get("body")),
        }
    elif command == "commits":
        commit = item.get("commit") or {}
        result = {
            "sha": item.get("sha"),
            "html_url": item.get("html_url"),
            "author": actor(item.get("author")),
            "committer": actor(item.get("committer")),
            "authored_at": (commit.get("author") or {}).get("date"),
            "committed_at": (commit.get("committer") or {}).get("date"),
            "message": cut(commit.get("message"), 1000),
        }
    else:
        result = dict(item)

    if matched:
        result["matched_queries"] = matched
    return result


def summarize(command: str, data: Any) -> Any:
    if command in {"search-repos", "search-issues", "search-code"}:
        result = {key: value for key, value in data.items() if key != "items"}
        result["items"] = [summarize_item(command, item) for item in data["items"]]
        return result
    if command in {"issues", "pulls", "releases", "commits"}:
        return {
            "returned_items": len(data),
            "items": [summarize_item(command, item) for item in data],
        }
    if command == "issue":
        return {
            "issue": summarize_item("issues", data["issue"]),
            "comments": [
                {
                    "html_url": comment.get("html_url"),
                    "user": actor(comment.get("user")),
                    "author_association": comment.get("author_association"),
                    "created_at": comment.get("created_at"),
                    "updated_at": comment.get("updated_at"),
                    "body": cut(comment.get("body")),
                }
                for comment in data.get("comments", [])
            ],
        }
    if command == "repo":
        return summarize_item("search-repos", data)
    if command in {"readme", "contents"} and isinstance(data, dict):
        return {
            "name": data.get("name"),
            "path": data.get("path"),
            "sha": data.get("sha"),
            "size": data.get("size"),
            "html_url": data.get("html_url"),
            "download_url": data.get("download_url"),
            "type": data.get("type"),
            "decoded_text": data.get("decoded_text"),
        }
    if command == "contents" and isinstance(data, list):
        return {
            "returned_items": len(data),
            "items": [
                {
                    "name": item.get("name"),
                    "path": item.get("path"),
                    "sha": item.get("sha"),
                    "size": item.get("size"),
                    "html_url": item.get("html_url"),
                    "download_url": item.get("download_url"),
                    "type": item.get("type"),
                }
                for item in data
            ],
        }
    return data


def rate_summary(headers: dict[str, str]) -> dict[str, str | None]:
    return {
        "limit": headers.get("x-ratelimit-limit"),
        "remaining": headers.get("x-ratelimit-remaining"),
        "used": headers.get("x-ratelimit-used"),
        "reset": headers.get("x-ratelimit-reset"),
        "resource": headers.get("x-ratelimit-resource"),
    }


def emit(
    command: str,
    data: Any,
    headers: dict[str, str],
    compact: bool,
    full: bool,
) -> None:
    payload = {
        "fetched_at": utc_now(),
        "command": command,
        "authentication": "token" if token() else "anonymous",
        "rate": rate_summary(headers),
        "data": data if full else summarize(command, data),
    }
    if command == "rate" and not token():
        payload["note"] = (
            "GitHub may report a code_search quota for anonymous requests, "
            "but the code search endpoint still requires authentication."
        )
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=None if compact else 2)
    sys.stdout.write("\n")


def add_page_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--per-page", type=int, default=30, choices=range(1, 101), metavar="1..100"
    )
    parser.add_argument(
        "--pages", type=int, default=1, choices=range(1, 11), metavar="1..10"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compact", action="store_true", help="emit compact JSON")
    parser.add_argument(
        "--full", action="store_true", help="emit full GitHub API objects instead of concise evidence fields"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("rate", help="show current API rate limits")

    repo_search = sub.add_parser("search-repos", help="search repositories")
    repo_search.add_argument("query", nargs="+", help="one or more quoted GitHub queries")
    repo_search.add_argument(
        "--sort", choices=["stars", "forks", "help-wanted-issues", "updated"]
    )
    repo_search.add_argument("--order", choices=["asc", "desc"], default="desc")
    add_page_options(repo_search)

    issue_search = sub.add_parser(
        "search-issues", help="search issues or pull requests"
    )
    issue_search.add_argument(
        "query", nargs="+", help="one or more quoted queries; include is:issue or is:pr when the distinction matters"
    )
    issue_search.add_argument(
        "--sort", choices=["comments", "interactions", "created", "updated"]
    )
    issue_search.add_argument("--order", choices=["asc", "desc"], default="desc")
    add_page_options(issue_search)

    code_search = sub.add_parser(
        "search-code", help="search code; GitHub normally requires authentication"
    )
    code_search.add_argument("query", nargs="+", help="one or more quoted GitHub queries")
    code_search.add_argument("--sort", choices=["indexed"])
    code_search.add_argument("--order", choices=["asc", "desc"], default="desc")
    add_page_options(code_search)

    repo = sub.add_parser("repo", help="get repository metadata")
    repo.add_argument("repository")

    issue = sub.add_parser("issue", help="get one issue and optionally its comments")
    issue.add_argument("repository")
    issue.add_argument("number", type=int)
    issue.add_argument("--comments", action="store_true")
    issue.add_argument(
        "--comment-pages",
        type=int,
        default=1,
        choices=range(1, 11),
        metavar="1..10",
    )

    for name, help_text in [
        ("issues", "list repository issues"),
        ("pulls", "list repository pull requests"),
        ("releases", "list repository releases"),
        ("commits", "list repository commits"),
    ]:
        cmd = sub.add_parser(name, help=help_text)
        cmd.add_argument("repository")
        add_page_options(cmd)
        if name in {"issues", "pulls"}:
            cmd.add_argument(
                "--state", choices=["open", "closed", "all"], default="all"
            )
        if name == "issues":
            cmd.add_argument(
                "--include-pulls",
                action="store_true",
                help="keep pull requests returned by the Issues endpoint",
            )
            cmd.add_argument("--labels")
            cmd.add_argument("--since")
        if name == "commits":
            cmd.add_argument("--since")
            cmd.add_argument("--until")
            cmd.add_argument("--path")

    readme = sub.add_parser("readme", help="get repository README")
    readme.add_argument("repository")
    readme.add_argument("--ref")
    readme.add_argument("--raw", action="store_true")

    contents = sub.add_parser(
        "contents", help="get a file or directory from a repository"
    )
    contents.add_argument("repository")
    contents.add_argument("path")
    contents.add_argument("--ref")
    contents.add_argument("--raw", action="store_true")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "rate":
            data, headers = request("/rate_limit")
        elif args.command in {"search-repos", "search-issues", "search-code"}:
            if args.command == "search-code" and not token():
                raise GitHubError(
                    "search-code requires GITHUB_TOKEN or GH_TOKEN; use raw files, "
                    "a local clone, or an authenticated browser as a fallback"
                )
            endpoint = {
                "search-repos": "/search/repositories",
                "search-issues": "/search/issues",
                "search-code": "/search/code",
            }[args.command]
            data, headers = search_many(
                endpoint,
                args.query,
                args.sort,
                args.order,
                args.per_page,
                args.pages,
            )
        elif args.command == "repo":
            data, headers = request(repo_path(args.repository))
        elif args.command == "issue":
            issue_data, headers = request(
                repo_path(args.repository, f"/issues/{args.number}")
            )
            comments_data: list[Any] = []
            if args.comments:
                comments_data, headers = paged(
                    repo_path(args.repository, f"/issues/{args.number}/comments"),
                    {"per_page": 100},
                    args.comment_pages,
                )
            data = {"issue": issue_data, "comments": comments_data}
        elif args.command in {"issues", "pulls", "releases", "commits"}:
            params: dict[str, Any] = {"per_page": args.per_page}
            if args.command in {"issues", "pulls"}:
                params["state"] = args.state
            if args.command == "issues":
                params.update({"labels": args.labels, "since": args.since})
            if args.command == "commits":
                params.update(
                    {"since": args.since, "until": args.until, "path": args.path}
                )
            data, headers = paged(
                repo_path(args.repository, f"/{args.command}"), params, args.pages
            )
            if args.command == "issues" and not args.include_pulls:
                data = [item for item in data if "pull_request" not in item]
        elif args.command in {"readme", "contents"}:
            if args.command == "readme":
                suffix = "/readme"
            else:
                suffix = f"/contents/{urllib.parse.quote(args.path, safe='/')}"
            accept = "application/vnd.github.raw+json" if args.raw else None
            data, headers = request(
                repo_path(args.repository, suffix), {"ref": args.ref}, accept=accept
            )
            if args.raw:
                sys.stdout.write(data)
                if data and not data.endswith("\n"):
                    sys.stdout.write("\n")
                return 0
            if (
                isinstance(data, dict)
                and data.get("encoding") == "base64"
                and isinstance(data.get("content"), str)
            ):
                data["decoded_text"] = base64.b64decode(data["content"]).decode(
                    "utf-8", errors="replace"
                )
            emit(args.command, data, headers, args.compact, args.full)
            return 0
        else:
            parser.error("unknown command")
            return 2
    except GitHubError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    emit(args.command, data, headers, args.compact, args.full)
    if args.command.startswith("search-"):
        return {"success": 0, "partial": 1, "error": 2}[data["outcome"]]
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
