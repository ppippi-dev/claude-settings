---
name: todo
description: Personal TODO management skill for private-memory repo. Use when user wants to manage personal tasks - add, list, complete, or remove todos. Triggers on /todo command or requests like "할일 추가", "TODO 확인", "할일 완료", "할일 삭제".
---

# Personal TODO Manager

Manage personal TODO items in `private-memory` repository.

## Repository Setup

- **Repo**: `~/repos/private-memory` (clone from github.com/ppippi-dev/private-memory)
- **Branch**: Always work on `main`

## File Structure

```
private-memory/
├── TODO.md              # Active todos
└── archive/
    └── YYYY-MM.md       # Completed todos by month
```

## First Step: Select Action

Use AskUserQuestion to ask which action:

| Action | Description |
|--------|-------------|
| **Add** (default) | Add new todo item |
| **List** | Show current todos |
| **Complete** | Mark todo as done → move to archive |
| **Remove** | Delete todo without archiving |

## Workflows

### Add

1. Ask for todo content (or use provided text)
2. Read `TODO.md`, append new item: `- [ ] {content}`
3. Commit & push: `todo: add "{content}"`

### List

1. Read and display `TODO.md`
2. Show numbered list for easy reference

### Complete

1. Read `TODO.md`, show numbered list
2. Ask which item(s) to complete
3. Remove from `TODO.md`
4. Append to `archive/YYYY-MM.md`: `- [x] {content} (YYYY-MM-DD)`
5. Create archive file if not exists
6. Commit & push: `todo: complete "{content}"`

### Remove

1. Read `TODO.md`, show numbered list
2. Ask which item(s) to remove
3. Remove from `TODO.md` (no archive)
4. Commit & push: `todo: remove "{content}"`

## TODO.md Format

```markdown
# TODO

- [ ] First task
- [ ] Second task
```

## Archive Format (archive/YYYY-MM.md)

```markdown
# Completed - YYYY-MM

- [x] Completed task (2025-01-19)
- [x] Another task (2025-01-18)
```

## Git Workflow

1. `cd ~/repos/private-memory`
2. `git pull origin main`
3. Make changes
4. `git add .`
5. `git commit -m "todo: {action} \"{content}\""`
6. `git push origin main`
