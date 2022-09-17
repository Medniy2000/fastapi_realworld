from typing import List, Any


def to_paginated_resp(data: List[Any], total_count: int) -> dict:
    return {"count": total_count, "results": data}
