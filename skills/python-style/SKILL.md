---
name: python-style
description: "Python 코드 작성 스타일 가이드. 파이써닉한 코드, 가독성, 로깅, 타입 힌트, 파일 구조 규칙. 사용 시점: (1) Python 코드 작성/수정 시, (2) Python 코드 리뷰 시, (3) Python 프로젝트 구조 설계 시."
---

# Python Code Style

## Core Principles

1. **파이써닉하고 간결한 코드**
   - 불필요한 코드/변수/로직 작성 금지
   - lazy import는 성능상 필요한 경우에만

2. **가독성 우선**
   - 명확한 변수/함수 이름
   - 복잡한 로직은 함수로 분리

## Logging

```python
# Good - lazy % formatting
logger.info("Processing %s items", count)
logger.error("Failed to process %s: %s", item_id, error)

# Avoid - f-string (항상 평가됨)
logger.info(f"Processing {count} items")
```

## Type Hints

```python
# Good
def process_items(items: list[str], limit: int = 10) -> dict[str, int]:
    ...

# Collections
from collections.abc import Sequence, Mapping

def filter_data(data: Sequence[int]) -> list[int]:
    ...
```

## Docstrings

```python
def calculate_total(items: list[Item], discount: float = 0.0) -> float:
    """Calculate total price with optional discount.

    Args:
        items: List of items to calculate.
        discount: Discount rate (0.0 to 1.0).

    Returns:
        Total price after discount.

    Raises:
        ValueError: If discount is not between 0 and 1.
    """
```

## Code Patterns

```python
# Good - list comprehension
result = [x * 2 for x in items if x > 0]

# Good - early return
def process(data):
    if not data:
        return None
    # main logic here

# Good - context manager
with open(path) as f:
    content = f.read()

# Avoid - nested conditions
if condition1:
    if condition2:
        if condition3:
            ...
```

## File Structure

- 한 파일에 과도한 코드 금지 (300-500줄 권장)
- 관련 기능끼리 모듈로 분리
- `__init__.py`에서 public API만 export
