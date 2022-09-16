from typing import Type, Callable

from starlette.requests import Request

from src.app.core.services.base import Service


def get_service(
    service_type: Type[Service],
) -> Callable:
    def get_service_inner(request: Request) -> Service:
        tmp_service_type = service_type(request)
        return tmp_service_type

    return get_service_inner
