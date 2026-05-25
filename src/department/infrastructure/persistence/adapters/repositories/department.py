
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from department.application.common.application_error import ApplicationError, ApplicationTypeError
from department.domain.department.entity import Department
from department.domain.department.repository import DepartmentRepository
from department.domain.department.value_objects import DepartmentId
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

    async def get_children_ids(self, parent_id: DepartmentId) -> list[DepartmentId]:
        stmt = select(DEPARTMENT_TABLE.c.id).where(
            DEPARTMENT_TABLE.c.parent_id == parent_id
        )
        result = await self.__session.execute(stmt)
        return [DepartmentId(row[0]) for row in result.all()]

    async def delete(self, entity: Department) -> None:
        await self.__session.delete(entity)

    async def exists(self, **filters: Any) -> bool:
        stmt = select(Department)
        stmt = self._add_filters(DEPARTMENT_TABLE, stmt, **filters)
        result = await self.__session.execute(stmt.limit(1))
        return result.scalar_one_or_none() is not None

    async def is_descendant(
        self,
        ancestor_id: DepartmentId,
        descendant_id: DepartmentId,
    ) -> bool:

        children = await self.get_children_ids(ancestor_id)

        for child_id in children:
            if child_id == descendant_id:
                return True

            if await self.is_descendant(
                child_id,
                descendant_id,
            ):
                return True

        return False