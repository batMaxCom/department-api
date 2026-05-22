from abc import ABC, abstractmethod

from department.domain.department.value_objects import DepartmentId
from department.domain.employee.entity import Employee


class EmployeeRepository(ABC):

    @abstractmethod
    async def add(self, entity: Employee) -> None:
        """Create new department"""

    @abstractmethod
    async def delete(self, entity: Employee) -> None:
        """Delete an employee."""

    @abstractmethod
    async def delete_by_department(self, department_id: DepartmentId) -> None:
        """Delete all employees in a department."""

    @abstractmethod
    async def reassign_to_department(
        self, from_id: DepartmentId, to_id: DepartmentId
    ) -> None:
        """Move all employees from one department to another."""
