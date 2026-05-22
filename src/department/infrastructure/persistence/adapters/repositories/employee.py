from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from department.domain.department.value_objects import DepartmentId
from department.domain.employee.entity import Employee
from department.domain.employee.repository import EmployeeRepository
from department.infrastructure.persistence.tables import EMPLOYEE_TABLE


class EmployeeRepositoryImpl(EmployeeRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, entity: Employee) -> None:
        self.__session.add(entity)

    async def delete(self, entity: Employee) -> None:
        await self.__session.delete(entity)

    async def delete_by_department(self, department_id: DepartmentId) -> None:
        stmt = select(Employee).where(
            EMPLOYEE_TABLE.c.department_id == department_id
        )
        result = await self.__session.execute(stmt)
        for employee in result.scalars().all():
            await self.__session.delete(employee)

    async def reassign_to_department(
        self, from_id: DepartmentId, to_id: DepartmentId
    ) -> None:
        stmt = (
            update(EMPLOYEE_TABLE)
            .where(EMPLOYEE_TABLE.c.department_id == from_id)
            .values(department_id=to_id)
        )
        await self.__session.execute(stmt)
