from dataclasses import dataclass

from department.application.common.dto.department import DepartmentDetailsDto
from department.application.ports.cqrs import QueryHandler, Query
from department.application.ports.gateways import DepartmentGateway
from department.domain.common.domain_errors import DomainError, DomainTypeError
from department.domain.department.value_objects import DepartmentId


@dataclass(frozen=True, slots=True)
class GetDepartmentQuery(Query[DepartmentDetailsDto]):
    department_id: int
    include_employees: bool
    depth: int = 1

    #ToDo: Следует убрать в value_objects
    def __post_init__(self) -> None:
        if self.depth < 1:
            raise DomainError(
                type=DomainTypeError.VALIDATION,
                message="Depth must be >= 1"
            )
        if self.depth > 5:
            raise DomainError(
                type=DomainTypeError.VALIDATION,
                message="Depth must be <= 5"
            )


class GetDepartmentQueryHandler(QueryHandler[GetDepartmentQuery, DepartmentDetailsDto]):
    def __init__(self, department_gateway: DepartmentGateway) -> None:
        self.__department_gateway = department_gateway

    async def handle(self, query: GetDepartmentQuery) -> DepartmentDetailsDto:
        return await self.__department_gateway.get_details(
            department_id=DepartmentId(query.department_id),
            depth=query.depth,
            include_employees=query.include_employees,
        )