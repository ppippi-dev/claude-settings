#!/usr/bin/env python3
"""
Fetch unresolved review threads from a GitHub PR using GraphQL API.

Usage:
    ./get_review_threads.py <owner> <repo> <pr_number> [--all]

Output: JSON array of review threads with comments
"""

import argparse
import json
import subprocess
import sys


GRAPHQL_QUERY = """
query($owner: String!, $repo: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $cursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          startLine
          diffSide
          comments(first: 100) {
            nodes {
              id
              author {
                login
              }
              body
              createdAt
              url
            }
          }
        }
      }
    }
  }
}
"""


RESOLVE_MUTATION = """
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread {
      id
      isResolved
    }
  }
}
"""


def run_gh_api(query: str, variables: dict) -> dict:
    """Execute GraphQL query using gh cli."""
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if isinstance(value, int):
            cmd.extend(["-F", f"{key}={value}"])
        else:
            cmd.extend(["-f", f"{key}={value}"])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    return json.loads(result.stdout)


def resolve_thread(thread_id: str) -> bool:
    """Resolve a single thread. Returns True on success."""
    cmd = [
        "gh", "api", "graphql",
        "-f", f"query={RESOLVE_MUTATION}",
        "-f", f"threadId={thread_id}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def fetch_all_threads(owner: str, repo: str, pr_number: int) -> list:
    """Fetch all review threads with pagination."""
    threads = []
    cursor = None

    while True:
        variables = {"owner": owner, "repo": repo, "number": pr_number}
        if cursor:
            variables["cursor"] = cursor

        data = run_gh_api(GRAPHQL_QUERY, variables)
        pr_data = data.get("data", {}).get("repository", {}).get("pullRequest", {})
        thread_data = pr_data.get("reviewThreads", {})

        nodes = thread_data.get("nodes", [])
        threads.extend(nodes)

        page_info = thread_data.get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")

    return threads


def format_thread(thread: dict) -> dict:
    """Format thread for output."""
    comments = thread.get("comments", {}).get("nodes", [])
    first_comment = comments[0] if comments else {}

    return {
        "thread_id": thread.get("id"),
        "is_resolved": thread.get("isResolved"),
        "is_outdated": thread.get("isOutdated"),
        "path": thread.get("path"),
        "line": thread.get("line"),
        "start_line": thread.get("startLine"),
        "diff_side": thread.get("diffSide"),
        "author": first_comment.get("author", {}).get("login"),
        "body": first_comment.get("body"),
        "url": first_comment.get("url"),
        "created_at": first_comment.get("createdAt"),
        "comment_count": len(comments),
        "all_comments": [
            {
                "author": c.get("author", {}).get("login"),
                "body": c.get("body"),
                "created_at": c.get("createdAt"),
            }
            for c in comments
        ],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Fetch review threads from a GitHub PR"
    )
    parser.add_argument("owner", help="Repository owner")
    parser.add_argument("repo", help="Repository name")
    parser.add_argument("pr_number", type=int, help="Pull request number")
    parser.add_argument(
        "--all", action="store_true", help="Include resolved threads (default: unresolved only)"
    )
    parser.add_argument(
        "--resolve-outdated", action="store_true", help="Auto-resolve outdated threads"
    )
    parser.add_argument(
        "--format", choices=["json", "summary"], default="json", help="Output format"
    )

    args = parser.parse_args()

    threads = fetch_all_threads(args.owner, args.repo, args.pr_number)
    formatted = [format_thread(t) for t in threads]

    if not args.all:
        formatted = [t for t in formatted if not t["is_resolved"]]

    # Auto-resolve outdated threads
    if args.resolve_outdated:
        resolved_count = 0
        remaining = []
        for t in formatted:
            if t["is_outdated"] and not t["is_resolved"]:
                if resolve_thread(t["thread_id"]):
                    resolved_count += 1
                    print(f"Auto-resolved outdated: {t['path']}:{t['line']}", file=sys.stderr)
                else:
                    remaining.append(t)
            else:
                remaining.append(t)
        formatted = remaining
        if resolved_count > 0:
            print(f"\nAuto-resolved {resolved_count} outdated thread(s)\n", file=sys.stderr)

    if args.format == "summary":
        for i, t in enumerate(formatted, 1):
            status = "[RESOLVED]" if t["is_resolved"] else "[OPEN]"
            outdated = " (outdated)" if t["is_outdated"] else ""
            print(f"\n{i}. {status}{outdated} {t['path']}:{t['line']}")
            print(f"   Author: {t['author']}")
            print(f"   Comment: {t['body'][:200]}..." if len(t['body']) > 200 else f"   Comment: {t['body']}")
            print(f"   URL: {t['url']}")
    else:
        print(json.dumps(formatted, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
