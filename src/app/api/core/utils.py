from typing import Optional, List, Any

from furl import furl
from starlette.requests import Request

from src.app.config.settings import settings


def _get_prev_url(url: str, step: int = settings.BATCH_SIZE) -> Optional[str]:
    prev_page = furl(url)
    prev_page.args["offset"] = int(prev_page.args.get("offset", 0)) - step
    prev_url = prev_page.url
    if prev_page.args["offset"] < 0:
        prev_url = None

    return prev_url


def _get_next_url(url: str, total_count: int, step: int = settings.BATCH_SIZE) -> Optional[str]:
    next_page = furl(url)
    next_page.args["offset"] = int(next_page.args.get("offset", 0)) + step

    next_url = next_page.url
    if next_page.args["offset"] >= total_count:
        next_url = None
    return next_url


def get_page_urls(url: str, total_count: int) -> tuple[Optional[str], Optional[str]]:
    return _get_prev_url(url), _get_next_url(url, total_count)


def to_paginated_resp(request: Request, data: List[Any], total_count: int) -> dict:
    prev_, next_ = get_page_urls(str(request.url), total_count)
    return {"prev": prev_, "next": next_, "count": total_count, "results": data}
