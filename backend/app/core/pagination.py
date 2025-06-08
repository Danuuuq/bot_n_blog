from typing import TypeVar

from fastapi import Query
from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseParamsFields

from app.core.variables import SettingFieldDB

T = TypeVar('T')

CustomPage = CustomizedPage[
    Page[T],
    UseParamsFields(
        size=Query(
            SettingFieldDB.DEFAULT_SIZE_PAGINATION,
            ge=1,
            le=SettingFieldDB.MAX_SIZE_PAGINATION),
    ),
]
