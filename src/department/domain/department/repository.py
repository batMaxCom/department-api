from abc import ABC, abstractmethod
from typing import Any

from department.domain.department.entity import Department


class DepartmentRepository(ABC):

    @abstractmethod
    async def add(self, entity: Department) -> None:
        """Create new department"""

    @abstractmethod
    async def update(self, entity: Department) -> None:
        """Update an existing department."""

    @abstractmethod
    async def get(self, **filters: Any) -> Department:
        """Get a department by id."""

    @abstractmethod
    async def delete(self, entity: Department) -> None:
        """Delete a department."""
