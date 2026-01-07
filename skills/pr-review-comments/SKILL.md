---
name: pr-review-comments
description: "PR 리뷰 코멘트를 확인하고 처리하는 워크플로우. 사용 시점: (1) GitHub PR URL 포함된 리뷰 요청 (예: github.com/owner/repo/pull/123 리뷰 확인해줘), (2) PR 리뷰 확인 요청 (예: 다음 PR의 리뷰를 확인하고 싶어 [URL]), (3) PR 코멘트 확인해줘, 리뷰 반영해줘 등의 요청, (4) /pr-review-comments 호출. unresolved 코멘트를 하나씩 확인하고, 반영이 필요하면 코드 수정 후 자동으로 resolve 처리함. (user) (user)"
---

# PR Review Comments

PR 리뷰 코멘트를 순차적으로 확인하고, 반영이 필요한 내용은 수정 후 자동으로 resolve 처리하는 워크플로우.

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
./scripts/get_review_threads.py <owner> <repo> <pr_number> --format summary --resolve-outdated
```

- unresolved 코멘트만 가져옴 (--all 옵션으로 전체 조회 가능)
- `--resolve-outdated`: outdated 코멘트를 자동으로 resolve 처리

### 2. 각 코멘트 순차 처리

코멘트별로 다음 프로세스 수행:

1. **코멘트 내용 확인** - 파일 경로, 라인, 코멘트 내용 파악
2. **관련 코드 읽기** - 해당 파일의 코드 컨텍스트 확인
3. **반영 여부 판단**
   - 반영 필요: 코드 수정 후 resolve
   - 반영 불필요: 사용자에게 스킵 이유 설명하고 다음으로 진행
4. **코드 수정 시 codex-search 활용** - 복잡하거나 확신이 없는 경우 second opinion 요청

### 3. Resolve 처리

코드 반영 완료 후 자동으로 resolve:

```bash
./scripts/resolve_thread.py <thread_id>
```

## 판단 기준

**반영해야 하는 경우:**
- 버그 수정 요청
- 코드 스타일/컨벤션 위반 지적
- 성능 개선 제안
- 보안 취약점 지적
- 명확한 로직 오류

**스킵 가능한 경우:**
- 단순 질문 (코드로 해결 불가)
- 이미 반영된 내용
- outdated 코멘트 → `--resolve-outdated` 옵션으로 자동 처리됨
- 의견 차이로 논의가 필요한 경우 (사용자 확인 필요)

## 예시 실행

```
사용자: https://github.com/socar-inc/ai-agent-platform/pull/123 리뷰 확인해줘

1. URL 파싱 → owner: socar-inc, repo: ai-agent-platform, pr_number: 123
2. get_review_threads.py socar-inc ai-agent-platform 123 --format summary --resolve-outdated
   → outdated 코멘트 2개 자동 resolve됨
3. 코멘트 1/2: src/api.py:42 "이 함수에 에러 핸들링 추가 필요"
   → 코드 읽기 → 에러 핸들링 추가 → resolve_thread.py <thread_id>
4. 코멘트 2/2: src/utils.py:15 "이 변수명이 뭔가요?"
   → 단순 질문이므로 스킵, 다음으로
5. 완료 보고
```

## 스크립트

### get_review_threads.py

PR의 리뷰 스레드 목록 조회 (GraphQL API 사용)

```bash
# 기본 (unresolved만)
./scripts/get_review_threads.py <owner> <repo> <pr_number>

# 전체 조회
./scripts/get_review_threads.py <owner> <repo> <pr_number> --all

# 요약 형식 + outdated 자동 resolve (권장)
./scripts/get_review_threads.py <owner> <repo> <pr_number> --format summary --resolve-outdated
```

### resolve_thread.py

리뷰 스레드 resolve/unresolve (GraphQL mutation 사용)

```bash
# Resolve
./scripts/resolve_thread.py <thread_id>

# Unresolve
./scripts/resolve_thread.py <thread_id> --unresolve
```
