from abc import ABC, abstractmethod

from department.domain.employee.entity import Employee


class EmployeeRepository(ABC):

    @abstractmethod
    async def add(self, entity: Employee) -> None:
        """Create new department"""
