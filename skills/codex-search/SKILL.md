---
name: codex-search
description: "Claude가 답변에 확신이 없거나 검증이 필요할 때 codex CLI로 second opinion을 얻음. 사용 시점: (1) WebSearch 결과가 불충분하거나 애매할 때, (2) 복잡한 코드/설계 결정에서 확신이 없을 때, (3) Claude가 작성한 코드의 적합성/품질 검증이 필요할 때, (4) 브레인스토밍이나 다양한 관점이 필요할 때, (5) 여러 선택지 중 최선을 결정하기 어려울 때."
---

# Codex Assistant

## 사용 방법

```bash
# 웹 검색 (네트워크 필요)
codex exec --skip-git-repo-check --sandbox danger-full-access "질문" 2>/dev/null

# 브레인스토밍/코드 리뷰 (네트워크 불필요)
codex exec --skip-git-repo-check --sandbox read-only "질문" 2>/dev/null
```

## 예시

```bash
# 웹 검색
codex exec --skip-git-repo-check --sandbox danger-full-access "쏘카 2026년 영업이익 전망" 2>/dev/null

# 브레인스토밍
codex exec --skip-git-repo-check --sandbox read-only "마이크로서비스 vs 모놀리식 장단점" 2>/dev/null
```

## 주의사항

- 웹 검색 시 `--sandbox danger-full-access` 필수
- codex 결과를 그대로 전달하지 말고 핵심만 요약하여 답변
- `2>/dev/null`로 생각 토큰 제외
