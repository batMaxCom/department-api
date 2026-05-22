
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from department.application.common.application_error import ApplicationError, ApplicationTypeError
from department.domain.department.entity import Department
from department.domain.department.repository import DepartmentRepository
from department.infrastructure.persistence.adapters.common.mixins import FilterMixin
from department.infrastructure.persistence.tables import DEPARTMENT_TABLE
from department.application.common.const import errors as error_texts


class DepartmentRepositoryImpl(DepartmentRepository, FilterMixin):

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, entity: Department) -> None:
        self.__session.add(entity)

    async def update(self, entity: Department) -> None:
        await self.__session.merge(entity)

    async def get(self, **filters: Any) -> Department:
        stmt = select(Department)
        stmt = self._add_filters(DEPARTMENT_TABLE, stmt, **filters)
        result = await self.__session.execute(stmt)
        departments = result.scalar_one_or_none()

        if not departments:
            raise ApplicationError(
                type=ApplicationTypeError.NOT_FOUND,
                message=error_texts.DEPARTMENT_NOT_FOUND
            )
        return departments


    async def delete(self, entity: Department) -> None:
        await self.__session.delete(entity)
