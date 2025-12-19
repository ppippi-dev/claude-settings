---
name: git-practices
description: "Git 커밋, 푸시, PR 작업을 위한 가이드. Conventional Commits 형식, 브랜치 네이밍, 시크릿 검사 포함. 사용 시점: (1) git commit 요청 시, (2) git push 요청 시, (3) PR 생성 요청 시, (4) 브랜치 생성/이름 관련 질문 시."
---

# Git Practices

## Commit Message Format (Conventional Commits)

```
<type>(<scope>): <description>

[optional body]
```

### Types

| Type | Description |
|------|-------------|
| feat | 새로운 기능 추가 |
| fix | 버그 수정 |
| docs | 문서 변경 |
| style | 코드 포맷팅 (기능 변경 없음) |
| refactor | 리팩토링 (기능/버그 수정 아님) |
| test | 테스트 추가/수정 |
| chore | 빌드, 설정 등 기타 변경 |

### Examples

```bash
# Good
git commit -m "feat(auth): add JWT token validation"
git commit -m "fix(api): resolve null pointer in payment flow"
git commit -m "docs(readme): update installation guide"

# Bad - avoid these patterns
git commit -m "fix stuff"
git commit -m "WIP"
git commit -m "Changes"
```

## Branch Naming

```
<type>/<ticket-id>-<short-description>
```

| Type | Purpose |
|------|---------|
| feature/ | 새 기능 개발 |
| bugfix/ | 버그 수정 |
| hotfix/ | 긴급 수정 (production) |
| release/ | 릴리즈 준비 |

**Examples:**
- `feature/AUTH-123-jwt-authentication`
- `bugfix/API-456-fix-null-pointer`
- `hotfix/PROD-789-critical-security-patch`

## Pre-Commit Checklist

1. **시크릿 검사**: API 키, 비밀번호, 토큰 등 민감 정보 확인
2. **디버그 코드 제거**: console.log, print 등 제거
3. **Python 프로젝트**: `uv run pre-commit run` 실행

## Commit Rules

- Claude 생성 표시 제거:
  - ❌ `🤖 Generated with [Claude Code]`
  - ❌ `Co-Authored-By: Claude`
- 간결하고 명확한 영어로 작성
- 현재 시제 사용 ("Add feature" not "Added feature")

## PR Creation

PR 생성 시 **references/pr-template.md** 참조.
