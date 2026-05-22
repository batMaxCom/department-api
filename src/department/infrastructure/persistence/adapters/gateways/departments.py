from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from department.application.common.dto import DepartmentDetailsDto, DepartmentDto, EmployeeDto
from department.application.ports.gateways.department import DepartmentGateway
from department.domain.department.entity import Department
from department.domain.department.value_objects import DepartmentId
from department.domain.employee.entity import Employee
from department.infrastructure.persistence.tables import DEPARTMENT_TABLE, EMPLOYEE_TABLE


class DepartmentGatewayImpl(DepartmentGateway):

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def get_details(
        self,
        department_id: DepartmentId,
        depth: int,
        include_employees: bool,
    ) -> DepartmentDetailsDto:

        department = await self._load_department(department_id)

        employees = []
        if include_employees:
            employees = await self._load_employees(department_id)

        children = await self._load_children(
            department_id,
            depth - 1,
            include_employees,
        )

        return DepartmentDetailsDto(
            department=DepartmentDto.from_entity(department),
            employees=[EmployeeDto.from_entity(e) for e in employees],
            children=children,
        )

    async def _load_children(
        self,
        parent_id: DepartmentId,
        depth: int,
        include_employees: bool,
    ) -> list[DepartmentDetailsDto]:

        if depth <= 0:
            return []

        result = await self._query_children(parent_id)

        children: list[DepartmentDetailsDto] = []

        for dept in result:
            employees = []

            if include_employees:
                employees = await self._load_employees(dept.entity_id)

            children.append(
                DepartmentDetailsDto(
                    department=DepartmentDto.from_entity(dept),
                    employees=[EmployeeDto.from_entity(e) for e in employees],
                    children=await self._load_children(
                        dept.entity_id,
                        depth - 1,
                        include_employees,
                    ),
                )
            )

        return children

    async def _load_department(
        self,
        department_id: DepartmentId,
    ) -> Department:
        stmt = select(Department).where(
            DEPARTMENT_TABLE.c.id == department_id
        )

        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def _load_employees(
        self,
        department_id: DepartmentId,
    ) -> list[Employee]:
        stmt = select(Employee).where(
            EMPLOYEE_TABLE.c.department_id == department_id
        ).order_by(EMPLOYEE_TABLE.c.full_name)

        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def _query_children(
        self,
        parent_id: DepartmentId,
    ) -> list[Department]:
        stmt = select(Department).where(
            DEPARTMENT_TABLE.c.parent_id == parent_id
        )

        result = await self._session.execute(stmt)
        return list(result.scalars().all())
