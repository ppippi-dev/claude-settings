---
description: "Git 커밋, 푸시, PR 작업 수행 (Conventional Commits)"
---

현재까지 작업한 내용을 커밋하고 푸시합니다.

## 첫 단계: 푸시 방식 선택

**반드시 AskUserQuestion 도구를 사용하여 사용자에게 질문하세요:**

- **선택지 1 (default)**: "Create branch and push" - 새 브랜치를 생성하여 푸시 (PR 워크플로우)
- **선택지 2**: "Push to main directly" - main 브랜치에 직접 푸시

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

---

## 워크플로우 A: 브랜치 생성 후 푸시 (PR 워크플로우)

1. **브랜치 생성**
   - 현재 브랜치 확인: `git branch --show-current`
   - main/master에 있다면 새 브랜치 생성 필수
   - `git checkout -b <type>/<short-description>`

2. **현재 변경사항 확인**
   - `git status`로 staged/unstaged 변경사항 확인
   - `git diff`로 각 파일의 변경 내용 파악

3. **Pre-Commit 검사**
   - 시크릿 검사: API 키, 비밀번호, 토큰 등 민감 정보 확인
   - 디버그 코드 제거: console.log, print 등 제거
   - 파일 끝 줄바꿈 검증
   - Python 프로젝트: `uv run pre-commit run` 실행

4. **커밋**
   - `git add [관련 파일들]`
   - `git commit -m "type(scope): 설명"`

5. **브랜치에 푸시**
   - `git push -u origin <branch>`

6. **완료 확인**
   - `git log --oneline -5`
   - `git status`

### Branch Naming

```
<type>/<short-description>
```

| Type | Purpose |
|------|---------|
| feature/ | 새 기능 개발 |
| bugfix/ | 버그 수정 |
| hotfix/ | 긴급 수정 |
| release/ | 릴리즈 준비 |

---

## 워크플로우 B: main 브랜치 직접 푸시

1. **main 브랜치 확인**
   - `git branch --show-current`로 현재 브랜치 확인
   - main이 아니면: `git checkout main && git pull origin main`

2. **현재 변경사항 확인**
   - `git status`로 staged/unstaged 변경사항 확인
   - `git diff`로 각 파일의 변경 내용 파악

3. **Pre-Commit 검사**
   - 시크릿 검사: API 키, 비밀번호, 토큰 등 민감 정보 확인
   - 디버그 코드 제거: console.log, print 등 제거
   - 파일 끝 줄바꿈 검증
   - Python 프로젝트: `uv run pre-commit run` 실행

4. **커밋**
   - `git add [관련 파일들]`
   - `git commit -m "type(scope): 설명"`

5. **main에 푸시**
   - `git push origin main`

6. **완료 확인**
   - `git log --oneline -5`
   - `git status`

---

## PR Creation (gh CLI) - 브랜치 워크플로우 전용

### PR Title Format

```
<type>(<scope>): <brief description>
```

### PR Body Template

```markdown
## Summary
-

## Changes
-

## Test Plan
- [ ] Unit tests 추가/수정
- [ ] 로컬 테스트 완료

## Related Issues
Closes #
```

### gh CLI Usage

```bash
# PR 생성
gh pr create --title "feat(auth): add login" --body "..."

# Draft PR 생성
gh pr create --draft --title "WIP: feature implementation"

# PR 상태 확인
gh pr status
gh pr checks
```

## Commit Rules

- 간결하고 명확한 영어로 작성
- 현재 시제 사용 ("Add feature" not "Added feature")
- 각 커밋은 독립적으로 의미가 있어야 함
- .env, credentials 등 민감한 파일은 커밋하지 않음
