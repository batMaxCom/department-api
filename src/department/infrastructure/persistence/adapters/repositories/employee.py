from sqlalchemy.ext.asyncio import AsyncSession

from department.domain.employee.entity import Employee
from department.domain.employee.repository import EmployeeRepository


class EmployeeRepositoryImpl(EmployeeRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, entity: Employee) -> None:
        self.__session.add(entity)
