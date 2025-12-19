---
name: helm-infra
description: "Helm 차트와 Kubernetes 인프라 작업 가이드. values.yaml 오버라이딩 규칙, helm template 검증, 배포 워크플로우. 사용 시점: (1) Helm 차트 수정/배포 요청 시, (2) values.yaml 관련 작업 시, (3) Kubernetes 리소스 설정 시, (4) helm install/upgrade 요청 시."
---

# Helm / Infrastructure

## Core Rules

1. **values.yaml 직접 수정 금지**
   - 항상 `values-<env>.yaml` 파일로 오버라이딩
   - 환경별 분리: `values-dev.yaml`, `values-staging.yaml`, `values-production.yaml`

2. **변경 전 반드시 검증**
   - `helm template`으로 렌더링 결과 확인 후 배포

## Workflow

```
1. values-<env>.yaml 수정
       ↓
2. helm template 검증
       ↓
3. helm upgrade --install
```

## Commands

```bash
# 렌더링 검증 (배포 전 필수)
helm template <release> ./chart -f values-<env>.yaml

# 특정 리소스만 확인
helm template <release> ./chart -f values-<env>.yaml | grep -A 50 "kind: Deployment"

# Dry-run 검증
helm upgrade --install <release> ./chart -f values-<env>.yaml --dry-run

# 실제 배포
helm upgrade --install <release> ./chart -f values-<env>.yaml

# 롤백
helm rollback <release> <revision>
```

## Values Override Example

```yaml
# values-production.yaml
replicaCount: 3

resources:
  limits:
    cpu: "2"
    memory: "4Gi"
  requests:
    cpu: "500m"
    memory: "1Gi"

ingress:
  enabled: true
  hosts:
    - host: api.example.com
```

## Troubleshooting

```bash
# 배포 상태 확인
helm status <release>
helm history <release>

# 리소스 확인
kubectl get all -l app.kubernetes.io/instance=<release>
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```
