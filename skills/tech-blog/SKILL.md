---
name: tech-blog
description: "테크블로그 글쓰기 가이드. Agent/MLOps/오픈소스 주제, 글 구조 설계, SEO 메타데이터 작성. 사용 시점: (1) 블로그 글 작성 요청 시, (2) 글 아웃라인/구조 설계 시, (3) 블로그 포스트 frontmatter 작성 시, (4) 기술 문서를 블로그 형식으로 변환 시."
---

# Tech Blog Writing

## Post Structure

```markdown
# [제목] - 명확하고 검색 가능한 제목

## 도입부 (Hook)
- 문제 상황 또는 독자의 pain point
- 이 글에서 다룰 내용 한 줄 요약

## 배경/맥락 (선택)
- 기술의 등장 배경, 필요성
- 관련 개념 간단 설명

## 본문
### 핵심 개념/구현
- 단계별 설명
- 코드 예시와 설명 교차 배치

### 실습/예제 (선택)
- 따라할 수 있는 구체적 예시

## 마무리
- 핵심 정리 (3줄 이내)
- 다음 단계 또는 추가 학습 자료
```

## Frontmatter Template

```yaml
---
title: "제목: 부제목 형식 권장"
date: YYYY-MM-DD
description: "검색 결과에 표시될 150자 이내 요약"
tags: [agent, mlops, opensource, tool-name]
categories: [MLOps, Agent, Tutorial, Deep-dive]
image: /images/posts/thumbnail.png  # OG 이미지
---
```

## SEO Checklist

1. **제목 (Title)**
   - 핵심 키워드를 앞에 배치
   - 50-60자 이내 권장
   - 예: `LangGraph 입문: Agent 워크플로우 구축하기`

2. **설명 (Description)**
   - 150자 이내
   - 글의 핵심 가치를 명확히 전달
   - 예: `LangGraph를 활용해 멀티 에이전트 워크플로우를 구축하는 방법을 단계별로 설명합니다.`

3. **태그 (Tags)**
   - 구체적인 기술명 포함: `langchain`, `langgraph`, `mlflow`
   - 일반 카테고리 포함: `agent`, `mlops`, `tutorial`

4. **URL Slug**
   - 영문 소문자, 하이픈 사용
   - 예: `langgraph-agent-workflow-guide`

## Writing Style

- **코드 먼저, 설명은 그 다음**
  ```python
  # 코드 블록
  agent = create_agent(llm, tools)
  ```
  위 코드는 LLM과 도구를 연결하여 에이전트를 생성합니다.

- **독자 레벨 명시**: 도입부에 "이 글은 Python 기초 지식이 있는 독자를 대상으로 합니다" 형태로

- **외부 링크**: 공식 문서, GitHub 저장소 등 출처 명시

## Title Examples

```
# Good
LangGraph로 멀티 에이전트 시스템 구축하기
MLflow로 LLM 실험 추적하는 3가지 방법
Ollama + LangChain: 로컬 LLM 에이전트 만들기

# Avoid
LangGraph 사용법
MLflow 정리
에이전트 만들기
```
