---
name: helm-infra
description: Helm 차트와 인프라 작업 가이드. values.yaml 오버라이딩, helm template 검증 규칙. Helm, Kubernetes, 인프라 설정 작업 시 사용.
---

# Helm / Infrastructure

## Instructions

1. **values.yaml 수정 금지**
   - values.yaml을 직접 수정하지 않음
   - 항상 `values-<name>.yaml` 파일로 오버라이딩

2. **변경 검증**
   - 수정 후에는 반드시 `helm template`을 통해 렌더링 결과를 검증

## Example

```bash
# values 오버라이드 파일 생성/수정
vim values-production.yaml

# 렌더링 검증
helm template my-release ./chart -f values-production.yaml

# 설치/업그레이드
helm upgrade --install my-release ./chart -f values-production.yaml
```