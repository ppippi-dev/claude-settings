---
description: "main 브랜치에 직접 커밋하고 푸시 (Conventional Commits)"
---

현재까지 작업한 내용을 main 브랜치에 직접 커밋하고 푸시합니다.

## Commit Message Format (Conventional Commits)

```
<type>(<scope>): <description>
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

## 수행 단계

1. **main 브랜치 확인**
   - `git branch --show-current`로 현재 브랜치 확인
   - main이 아니면: `git checkout main && git pull origin main`

2. **현재 변경사항 확인**
   - `git status`로 staged/unstaged 변경사항 확인
   - `git diff`로 각 파일의 변경 내용 파악

3. **Pre-Commit 검사**
   - 시크릿 검사: API 키, 비밀번호, 토큰 등 민감 정보 확인
   - 디버그 코드 제거: console.log, print 등 제거
   - 파일 끝 줄바꿈 검증: 모든 파일이 newline으로 끝나는지 확인
   - Python 프로젝트: `uv run pre-commit run` 실행

4. **커밋**
   - `git add [관련 파일들]`
   - Conventional Commits 형식으로 커밋 메시지 작성
   - `git commit -m "type(scope): 설명"`

5. **main에 푸시**
   - `git push origin main`

6. **완료 확인**
   - `git log --oneline -5`으로 커밋 이력 확인
   - `git status`로 상태 확인

## Commit Rules

- Claude 생성 표시 제거:
  - ❌ `🤖 Generated with [Claude Code]`
  - ❌ `Co-Authored-By: Claude`
- 간결하고 명확한 영어로 작성
- 현재 시제 사용 ("Add feature" not "Added feature")
- .env, credentials 등 민감한 파일은 커밋하지 않음
