from abc import ABC, abstractmethod
from typing import Any

from domain.employee.employee import Employee


class EmployeeRepository(ABC):

    @abstractmethod
    async def add(self, entity: Employee) -> None:
        """Create new department"""

    @abstractmethod
    async def update(self, entity: Employee) -> None:
        """Update an existing employee."""

    @abstractmethod
    async def get(self, **filters: Any) -> Employee:
        """Get employee by id."""

    @abstractmethod
    async def delete(self, entity: Employee) -> None:
        """Delete employee."""

    @abstractmethod
    async def exists(self, **filters: Any) -> bool:
        """Check if employee exists."""