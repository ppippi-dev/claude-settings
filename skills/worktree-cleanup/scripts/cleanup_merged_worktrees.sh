#!/bin/bash
# Cleanup worktrees whose PRs have been merged

set -e

MAIN_REPO=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
if [ -z "$MAIN_REPO" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

echo "Checking worktrees for merged PRs..."
echo ""

CLEANED=0
SKIPPED=0

while IFS= read -r line; do
    # Parse worktree list output: /path/to/worktree commit [branch]
    WORKTREE_PATH=$(echo "$line" | awk '{print $1}')
    # Extract branch name between brackets
    BRANCH=$(echo "$line" | sed -n 's/.*\[\(.*\)\].*/\1/p')

    # Skip if no branch (detached HEAD) or if it's the main worktree
    if [ -z "$BRANCH" ] || [ "$WORKTREE_PATH" = "$MAIN_REPO" ]; then
        continue
    fi

    # Check if PR for this branch is merged
    PR_STATE=$(gh pr list --head "$BRANCH" --state merged --json state --jq '.[0].state' 2>/dev/null || echo "")

    if [ "$PR_STATE" = "MERGED" ]; then
        echo "Removing worktree: $WORKTREE_PATH (branch: $BRANCH) - PR merged"
        git worktree remove "$WORKTREE_PATH" --force 2>/dev/null || {
            echo "  Warning: Could not remove worktree, trying with force..."
            rm -rf "$WORKTREE_PATH"
            git worktree prune
        }
        ((CLEANED++))
    else
        echo "Keeping worktree: $WORKTREE_PATH (branch: $BRANCH) - PR not merged"
        ((SKIPPED++))
    fi
done < <(git worktree list)

echo ""
echo "Summary: Cleaned $CLEANED worktree(s), Skipped $SKIPPED worktree(s)"
