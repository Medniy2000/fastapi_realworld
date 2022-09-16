from abc import ABC

from starlette.requests import Request


class AbstractService(ABC):
    pass


class BaseService(AbstractService):
    def __init__(self, request: Request) -> None:
        self._request = request

    @property
    def request(self) -> Request:
        return self._request


class Service(BaseService):
    pass
