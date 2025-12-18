---
name: git-practices
description: Git 커밋 메시지 작성 규칙과 코드 리뷰 가이드. 커밋 메시지 형식, 시크릿 검사. git commit, push, 코드 커밋 작업 시 사용.
---

# Git Practices

## Instructions

1. **Commit 메시지 규칙**
   - claude가 작업했다는 표현 포함 금지 
      - 🤖 Generated with [Claude Code](https://claude.com/claude-code)
      - Co-Authored-By: Claude Opus 4.5
   - 간단하고 명확한 영어로 작성
   

2. **Commit 전 코드 리뷰**
   - 작업한 코드가 git에 올라가도 되는지 평가
   - 시크릿 정보(API 키, 비밀번호, 토큰 등) 포함 여부 확인
   - 문제가 있으면 커밋 전에 알림

## Checklist Before Commit

- [ ] **Python 프로젝트**: `uv run pre-commit run` 실행하여 통과 확인
- [ ] 시크릿/민감 정보 없음
- [ ] 불필요한 디버그 코드 제거
- [ ] 커밋 메시지가 변경 내용을 명확히 설명

## Example

```bash
# Good commit messages
git commit -m "Add user authentication endpoint"
git commit -m "Fix null pointer in payment processing"
git commit -m "Refactor database connection pooling"

# Bad (avoid)
git commit -m "Changes by Claude"
git commit -m "Fix stuff"
```