---
name: mem-analyzer
description: "claude-mem 대화 기록을 분석하여 스킬, 훅, settings.json, CLAUDE.md 추천 생성. 사용 시점: (1) /mem-analyzer 명령 호출 시, (2) 워크플로우 개선이 필요할 때, (3) 반복 작업 패턴을 스킬로 만들고 싶을 때."
---

# Mem Analyzer

claude-mem에 저장된 대화 기록을 분석하여 워크플로우 개선을 위한 추천을 생성한다.

## 워크플로우

### Step 1: 데이터 수집

MCP 도구로 전체 observations 조회:

```
1. search로 전체 기록 인덱스 조회 (limit: 1000)
2. get_observations로 상세 내용 가져오기
```

observations 타입:
- decision: 의사결정
- bugfix: 버그 수정
- feature: 기능 구현
- refactor: 리팩토링
- discovery: 발견/학습
- change: 변경사항

### Step 2: 패턴 분석

[references/analysis-prompts.md](references/analysis-prompts.md) 참조하여 다음 패턴 분석:

1. **반복 작업**: 같은 유형의 작업이 여러 세션에서 반복되는 패턴
2. **도구/명령어**: 자주 사용하는 도구나 명령어 패턴
3. **파일/디렉토리**: 자주 수정하는 파일이나 디렉토리 패턴
4. **의사결정**: 반복되는 의사결정 패턴

### Step 3: 추천 생성

각 패턴에 대해 추천 생성:

| 패턴 유형 | 추천 대상 |
|----------|----------|
| 반복 워크플로우 | 새 스킬 제안 |
| 자동화 가능한 트리거 | hook 설정 제안 |
| 환경 설정 관련 | settings.json 수정 제안 |
| 워크플로우 규칙 | CLAUDE.md 추가 제안 |

### Step 4: 결과 저장

결과를 마크다운 파일로 저장:
- 경로: `~/.claude/recommendations/YYYY-MM-DD-mem-analysis.md`
- 디렉토리가 없으면 생성

### Step 5: 분석 완료 세션 삭제

분석 완료된 세션을 claude-mem DB에서 삭제:

```bash
sqlite3 ~/.claude-mem/claude-mem.db "DELETE FROM sdk_sessions WHERE memory_session_id IN ('session_id_1', 'session_id_2', ...)"
```

주의사항:
- **현재 활성 세션은 제외** (status='active'이고 가장 최근 세션)
- CASCADE 삭제로 관련 observations, summaries, prompts 모두 삭제됨
- 삭제 전 결과 파일에 세션 ID 목록 기록 완료 확인

## 출력 파일 형식

```markdown
# Claude-Mem 분석 결과 (YYYY-MM-DD)

## 분석 요약
- 분석된 세션 수: N개
- 분석 기간: YYYY-MM-DD ~ YYYY-MM-DD
- observation 수: N개

## 스킬 추천
### 1. [스킬명]
- **근거:** 반복 패턴 설명
- **제안 내용:** 스킬이 할 일 설명

## 훅 추천
### 1. [훅 유형]
- **근거:** 자동화 필요성 설명
- **제안 설정:** hook 설정 예시 (JSON)

## settings.json 추천
### 1. [설정 항목]
- **현재 값:** (있는 경우)
- **제안 값:** 값
- **근거:** 이유

## CLAUDE.md 추천
### 1. [규칙 제목]
- **추가 규칙:** 규칙 내용
- **근거:** 이유

## 정리 대상 세션
분석에 사용된 세션 ID 목록:
- session_id_1
- session_id_2
...
```
