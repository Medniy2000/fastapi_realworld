# type: ignore
from abc import ABC
from typing import List, Any, Optional

from sqlalchemy.engine.result import RowProxy
from sqlalchemy.sql.selectable import Select

from src.app.config.settings import settings
from src.app.extensions.db import db


class AbstractRepository(ABC):
    pass


class BaseAbstractRepository(AbstractRepository):
    @classmethod
    async def count(
        cls,
        filter_data: dict,
    ) -> Any:
        raise NotImplementedError

    @classmethod
    async def exists(
        cls,
        filter_data: Optional[dict],
    ) -> bool:
        raise NotImplementedError

    @classmethod
    async def get_first_partial(cls, fields: Optional[list], filter_data: Optional[dict]) -> Any:
        raise NotImplementedError

    @classmethod
    async def get_list_partial(
        cls,
        fields: Optional[list],
        filter_data: Optional[dict],
        order_data: Optional[list],
        limit: Optional[int],
        offset: Optional[int],
    ) -> List[Any]:
        raise NotImplementedError

    @classmethod
    async def get_first(cls, filter_data: Optional[dict]) -> Any:
        raise NotImplementedError

    @classmethod
    async def get_list(
        cls,
        filter_data: Optional[dict],
        order_data: Optional[list],
        limit: Optional[int],
        offset: Optional[int],
    ) -> List[Any]:
        raise NotImplementedError

    @classmethod
    async def create(cls, data: dict) -> Any:
        raise NotImplementedError

    @classmethod
    async def update(cls, filter_data: dict, data: dict, return_updated=False) -> Any:
        raise NotImplementedError

    @classmethod
    async def update_by_obj(cls, obj: RowProxy, data: dict) -> Any:
        raise NotImplementedError

    @classmethod
    async def get_or_create(cls, filter_data: dict, data: dict) -> Any:
        raise NotImplementedError

    @classmethod
    async def delete(cls, filter_data: dict) -> bool:
        raise NotImplementedError


class BasePSQLRepository(BaseAbstractRepository):
    _ATR_SEPARATOR = "__"
    COMPARE_OPERATORS_MAP: dict = {
        "lt": "<",
        "lte": "<=",
        "gt": ">",
        "gte": ">=",
        "ne": "!=",
        "e": "==",
    }
    LOOKUP_MAP = {
        "<": lambda q, k, v: q.where(k < v),
        "<=": lambda q, k, v: q.where(k <= v),
        ">": lambda q, k, v: q.where(k > v),
        ">=": lambda q, k, v: q.where(k >= v),
        "!=": lambda q, k, v: q.where(k != v),
        "==": lambda q, k, v: q.where(k == v),
    }
    MODEL: db = None
    FIELDS_TO_SELECT: Optional[list] = []
    FIELDS_ORDER_BY: Optional[list] = ["-id"]

    @classmethod
    def __parsed_filter_key(cls, key: str) -> tuple[str, str]:
        splatted: list = key.split(cls._ATR_SEPARATOR)
        key_parsed = key
        if len(splatted) == 1:
            return key_parsed, "=="
        elif len(splatted) == 2:
            key_parsed = splatted[0]
            tmp_operator = splatted[1]
            lookup_parsed = cls.COMPARE_OPERATORS_MAP.get(tmp_operator)
            if not lookup_parsed:
                raise ValueError(f"Not supported format of {key}")
            return key_parsed, lookup_parsed
        raise ValueError(f"Not supported format of {key}")

    @classmethod
    def __apply_condition(cls, query: Select, key: str, value: Any) -> Select:
        parsed_key, parsed_lookup = cls.__parsed_filter_key(key)
        column = getattr(cls.MODEL, parsed_key, None)
        if column is None:
            raise ValueError(f"Not supported attr {parsed_key} for model {cls.MODEL}")
        func_ = cls.LOOKUP_MAP.get(parsed_lookup)
        if not func_:
            raise ValueError(f"Not supported lookup {parsed_lookup}")
        return func_(query, column, value)

    @classmethod
    def get_query_filtered(cls, query: Select, filter_data: Optional[dict] = None) -> Select:
        if not filter_data:
            filter_data = {}
        for k, v in filter_data.items():
            query = cls.__apply_condition(query, k, v)
        return query

    @classmethod
    def ordering_fields(cls, fields_to_order: List[str]) -> list:
        prepared_fields: list = []
        for item in fields_to_order:
            if item.startswith("-"):
                field = getattr(cls.MODEL, item[1:], None)
                if field is not None:
                    prepared_fields.append(field.desc())
                else:
                    raise ValueError(f"Not supported field {item} to ordering")
            else:
                field = getattr(cls.MODEL, item, None)
                if field is not None:
                    prepared_fields.append(field.asc())
                else:
                    raise ValueError(f"Not supported field {item} to ordering")
        return prepared_fields

    @classmethod
    async def count(cls, filter_data: Optional[dict] = None) -> int:
        """
        :param filter_data: dict - filter rows data
        :return: int - count of rows
        """
        if not filter_data:
            filter_data = {}

        q = db.func.count(cls.MODEL.id).select()  # type: ignore
        q = cls.get_query_filtered(q, filter_data)
        return await q.gino.scalar()

    @classmethod
    async def exists(
        cls,
        filter_data: Optional[dict],
    ) -> bool:
        """
        :param filter_data: dict - filter row data
        :return:
        """
        q = db.func.exists(cls.MODEL.id).select()  # type: ignore
        q = cls.get_query_filtered(q, filter_data)
        return await q.gino.scalar()

    @classmethod
    async def get_first_partial(
        cls,
        fields: Optional[list] = None,
        filter_data: Optional[dict] = None,
    ) -> Optional[RowProxy]:
        """
        :param filter_data: dict - filter row data
        :param fields: list[str] - fields to select.
        :return: RowProxy - row from database, if exists.
        """
        if not fields:
            fields = cls.FIELDS_TO_SELECT

        if not filter_data:
            filter_data = {}

        q = cls.MODEL.select(*fields)
        q = cls.get_query_filtered(q, filter_data)

        row = await q.gino.first()
        return row

    @classmethod
    async def get_list_partial(
        cls,
        fields: Optional[list] = None,
        filter_data: Optional[dict] = None,
        order_by: Optional[list] = None,
        limit: Optional[int] = settings.BATCH_SIZE,
        offset: Optional[int] = 0,
    ) -> List[RowProxy]:
        """
        :param fields: list - fields to select from db
        :param filter_data: dict - filter rows data
        :param order_by:  list - ordering fields
        :param limit: int - limit rows count to select
        :param offset: int - offset rows count to select
        :return: list
        """
        if not fields:
            fields = cls.FIELDS_TO_SELECT
        if not filter_data:
            filter_data = {}
        if not order_by:
            order_by = cls.FIELDS_ORDER_BY
        order_by_fields = cls.ordering_fields(order_by)  # type: ignore

        q = cls.MODEL.select(*fields)  # type: ignore
        q = cls.get_query_filtered(q, filter_data).order_by(*order_by_fields)
        return await q.offset(offset).limit(limit).gino.all()

    @classmethod
    async def get_first(cls, filter_data: Optional[dict]) -> Optional[db.Model]:
        """
        :param filter_data: dict - filter row data
        :return: Model - row from database, if exists.
        """

        if not filter_data:
            filter_data = {}

        q = cls.MODEL.query
        q = cls.get_query_filtered(q, filter_data)

        row = await q.gino.first()
        return row

    @classmethod
    async def get_list(
        cls,
        filter_data: Optional[dict] = None,
        order_by: Optional[list] = None,
        limit: Optional[int] = settings.BATCH_SIZE,
        offset: Optional[int] = 0,
    ) -> List[db.Model]:
        """
        :param filter_data: dict - filter rows data
        :param order_by:  list - ordering fields
        :param limit: int - limit rows count to select
        :param offset: int - offset rows count to select
        :return: list
        """
        if not filter_data:
            filter_data = {}
        if not order_by:
            order_by = cls.FIELDS_ORDER_BY
        order_by_fields = cls.ordering_fields(order_by)  # type: ignore

        q = cls.MODEL.query  # type: ignore
        q = cls.get_query_filtered(q, filter_data).order_by(*order_by_fields)
        return await q.offset(offset).limit(limit).gino.all()

    @classmethod
    async def create(cls, data: dict) -> db.Model:
        """
        :param data: dict - data to create new row
        :return: row
        """
        return await cls.MODEL.create(**data)  # type: ignore

    @classmethod
    async def update(cls, filter_data: dict, data: dict, return_updated=True) -> Optional[db.Model]:
        """
        :param filter_data: dict - data to update row
        :param data: dict - data to update row

        :param return_updated: bool - flag to mark is row updated require to return
        :return: row
        """
        q = cls.MODEL.update.values(**data)
        q = cls.get_query_filtered(q, filter_data=filter_data)

        if return_updated:
            return (
                await q.returning(*[getattr(cls.MODEL, item) for item in cls.FIELDS_TO_SELECT])
                .gino.model(cls.MODEL)
                .first()
            )

        return await q.gino.model(cls.MODEL).apply()

    @classmethod
    async def update_by_obj(cls, obj: db.Model, data: dict) -> db.Model:
        """
        :param obj: row obj to update
        :param data: dict - data to update row
        :return: row
        """
        return (
            await cls.MODEL.update.values(**data)
            .where(getattr(cls.MODEL, "id") == obj.id)
            .returning(*[getattr(cls.MODEL, item) for item in cls.FIELDS_TO_SELECT])
            .gino.model(cls.MODEL)
            .first()
        )

    @classmethod
    async def get_or_create(cls, filter_data: dict, data: dict) -> db.Model:
        """
        :param filter_data: dict - filter row(s) data
        :param data: dict - data to create new row
        :return: row
        """
        row = await cls.get_first(filter_data=filter_data)
        if not row:
            row = await cls.create(data)
        return row

    @classmethod
    async def update_or_create(cls, field: str, value: Any, data: dict) -> db.Model:
        """
        :param data: dict - data to update row
        :param value: any type - value parameter to get or update row
        :param field: field name parameter to get or update row
        :return: row
        """

        row = await cls.update(filter_data={field: value}, data=data)
        if not row:
            row = await cls.create(data)
        return row

    @classmethod
    async def delete(cls, filter_data: dict) -> bool:
        """
        :param filter_data: dict - filter row(s) data
        :return: bool - result status
        """
        q = cls.MODEL.delete  # type: ignore
        q = cls.get_query_filtered(q, filter_data)
        status = await q.gino.status()
        status_str_split = status[0].split(" ")
        count_str = status_str_split[1]
        return int(count_str) > 0
