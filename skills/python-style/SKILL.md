---
name: python-style
description: 파이썬 코드 작성 스타일 가이드. 파이써닉한 코드, 가독성, logger 사용, 주석/docstring, 파일 구조에 대한 규칙. Python 코드 작성, 수정, 리뷰 시 사용.
---

# Python Code Style

## Instructions

1. **파이써닉하고 가독성 높은 코드 우선**
   - 불필요한 코드, 변수, 로직은 작성하지 않으며, 보이면 제거
   - 성능에 큰 영향을 주지 않는 한 lazy import는 사용하지 않음

2. **Logger 사용**
   - Lazy % 또는 % formatting 사용
   ```python
   # Good
   logger.info("Processing %s items", count)

   # Avoid
   logger.info(f"Processing {count} items")
   ```

3. **주석과 문서화**
   - 주석은 꼭 필요한 경우에만 작성
   - 설명은 docstring으로 표현

4. **파일 구조**
   - 한 파일에 과도한 양의 코드를 넣지 않음
   - 논리적으로 적절하게 분리