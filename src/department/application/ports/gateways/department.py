from abc import ABC, abstractmethod

from department.application.common.dto.department import DepartmentDetailsDto
from department.domain.department.value_objects.department_id import DepartmentId


class DepartmentGateway(ABC):

    @abstractmethod
    async def get_details(
        self,
        department_id: DepartmentId,
        depth: int,
        include_employees: bool,
    ) -> DepartmentDetailsDto:
        """Returns fully built department tree projection."""