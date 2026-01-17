---
name: pr-review-comments
description: "PR 리뷰 코멘트를 확인하고 처리하는 워크플로우. 사용 시점: (1) GitHub PR URL 포함된 리뷰 요청 (예: github.com/owner/repo/pull/123 리뷰 확인해줘), (2) PR 리뷰 확인 요청 (예: 다음 PR의 리뷰를 확인하고 싶어 [URL]), (3) PR 코멘트 확인해줘, 리뷰 반영해줘 등의 요청, (4) /pr-review-comments 호출. unresolved 코멘트를 하나씩 확인하고, 반영이 필요하면 코드 수정 후 자동으로 resolve 처리함. (user) (user)"
---

# PR Review Comments

PR 리뷰 코멘트를 순차적으로 확인하고, 반영이 필요한 내용은 수정 후 자동으로 resolve 처리하는 워크플로우.

## 스크립트 실행 경로

스크립트 실행 시 반드시 `~` 경로를 사용:

```bash
~/.claude/skills/pr-review-comments/scripts/get_review_threads.py
~/.claude/skills/pr-review-comments/scripts/resolve_thread.py
```

절대경로(`/Users/...`)가 아닌 `~/.claude/...` 형식을 사용할 것.

## 워크플로우

### 0. PR 정보 파싱

GitHub PR URL에서 정보 추출:
- URL 형식: `https://github.com/{owner}/{repo}/pull/{pr_number}`
- 예: `https://github.com/socar-inc/ai-agent-platform/pull/123`
  - owner: `socar-inc`
  - repo: `ai-agent-platform`
  - pr_number: `123`

### 1. PR 코멘트 조회

```bash
~/.claude/skills/pr-review-comments/scripts/get_review_threads.py <owner> <repo> <pr_number> --format summary --resolve-outdated
```

- unresolved 코멘트만 가져옴 (--all 옵션으로 전체 조회 가능)
- `--resolve-outdated`: outdated 코멘트를 자동으로 resolve 처리

### 2. 각 코멘트 순차 처리

코멘트별로 다음 프로세스 수행:

1. **코멘트 내용 확인** - 파일 경로, 라인, 코멘트 내용 파악
2. **관련 코드 읽기** - 해당 파일의 코드 컨텍스트 확인
3. **반영 여부 판단 및 처리**
   - 반영 필요: 코드 수정 후 resolve
   - 반영 불필요: 스킵 이유 설명 후 **자동 resolve** (단순 질문, 사소한 의견 등)
   - 논의 필요: 사용자에게 확인 요청 (resolve 하지 않음)

### 3. Resolve 처리

코드 반영 완료 후 자동으로 resolve:

```bash
~/.claude/skills/pr-review-comments/scripts/resolve_thread.py <thread_id>
```

## 판단 기준

**반영해야 하는 경우:**
- 버그 수정 요청
- 코드 스타일/컨벤션 위반 지적
- 성능 개선 제안
- 보안 취약점 지적
- 명확한 로직 오류

**스킵 + 자동 resolve:**
- 단순 질문 (코드로 해결 불가) → 답변/설명 후 resolve
- 이미 반영된 내용 → resolve
- 사소한 스타일 의견 (PR 범위 벗어남) → 설명 후 resolve
- outdated 코멘트 → `--resolve-outdated` 옵션으로 자동 처리됨

**resolve 하지 않고 사용자 확인 필요:**
- 중요한 아키텍처/설계 의견 차이
- 비즈니스 로직 관련 판단이 필요한 경우

## 머지 가능 여부 판단

모든 코멘트 처리 완료 후, 머지 가능 여부를 판단하여 사용자에게 의견 제시:

**머지 가능:**
- 모든 unresolved 코멘트가 처리됨 (반영 또는 정당한 사유로 resolve)
- CI/테스트가 통과 상태 (확인 가능한 경우)
- 남은 논의 사항 없음

**머지 보류 권장:**
- 사용자 확인이 필요한 unresolved 코멘트 존재
- 중요한 설계/아키텍처 논의 미해결
- Blocker로 지정된 코멘트 존재

**판단 예시:**
```
✅ 머지 가능: 모든 리뷰 코멘트가 처리되었습니다. (3개 반영, 2개 스킵 resolve)
⚠️ 머지 보류: 2개 코멘트가 사용자 확인 대기 중입니다.
```

## 예시 실행

```
사용자: https://github.com/socar-inc/ai-agent-platform/pull/123 리뷰 확인해줘

1. URL 파싱 → owner: socar-inc, repo: ai-agent-platform, pr_number: 123
2. ~/.claude/skills/pr-review-comments/scripts/get_review_threads.py socar-inc ai-agent-platform 123 --format summary --resolve-outdated
   → outdated 코멘트 2개 자동 resolve됨
3. 코멘트 1/3: src/api.py:42 "이 함수에 에러 핸들링 추가 필요"
   → 코드 읽기 → 에러 핸들링 추가 → resolve_thread.py <thread_id>
4. 코멘트 2/3: src/utils.py:15 "이 변수명이 뭔가요?"
   → 단순 질문 → 변수명 설명 후 resolve_thread.py <thread_id>
5. 코멘트 3/3: src/config.py:8 "이 설정 방식 재검토 필요"
   → 아키텍처 논의 필요 → 사용자에게 확인 요청 (resolve 하지 않음)
6. 머지 가능 여부 판단:
   ⚠️ 머지 보류: 1개 코멘트가 사용자 확인 대기 중입니다. (2개 반영, 1개 스킵 resolve)
```

## 스크립트

### get_review_threads.py

PR의 리뷰 스레드 목록 조회 (GraphQL API 사용)

```bash
# 기본 (unresolved만)
~/.claude/skills/pr-review-comments/scripts/get_review_threads.py <owner> <repo> <pr_number>

# 전체 조회
~/.claude/skills/pr-review-comments/scripts/get_review_threads.py <owner> <repo> <pr_number> --all

# 요약 형식 + outdated 자동 resolve (권장)
~/.claude/skills/pr-review-comments/scripts/get_review_threads.py <owner> <repo> <pr_number> --format summary --resolve-outdated
```

### resolve_thread.py

리뷰 스레드 resolve/unresolve (GraphQL mutation 사용)

```bash
# Resolve
~/.claude/skills/pr-review-comments/scripts/resolve_thread.py <thread_id>

# Unresolve
~/.claude/skills/pr-review-comments/scripts/resolve_thread.py <thread_id> --unresolve
```
