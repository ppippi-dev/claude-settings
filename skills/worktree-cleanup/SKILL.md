---
name: worktree-cleanup
description: Clean up git worktrees whose PRs have been merged. Use when user asks to clean worktrees, check for merged worktrees, remove old worktrees, or mentions "worktree cleanup", "정리", or wants to clean up after PR merges.
---

# Worktree Cleanup

Clean up git worktrees whose associated PRs have been merged.

## Workflow

1. Run the cleanup script from the main repository:

```bash
/Users/ppippi/.claude/skills/worktree-cleanup/scripts/cleanup_merged_worktrees.sh
```

2. The script will:
   - List all worktrees
   - Check each worktree's branch for merged PR status via `gh pr list`
   - Remove worktrees with merged PRs using `git worktree remove`
   - Report summary of cleaned and skipped worktrees

## Manual Cleanup

If needed, manually remove a specific worktree:

```bash
git worktree remove /path/to/worktree --force
git worktree prune
```

## Requirements

- `gh` CLI authenticated with GitHub
- Git repository with worktrees
