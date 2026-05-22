from dishka import Provider, Scope, provide

from department.domain.department.repository import DepartmentRepository
from department.domain.employee.repository import EmployeeRepository
from department.infrastructure.persistence.adapters.repositories import (
    DepartmentRepositoryImpl, EmployeeRepositoryImpl
)

REPOSITORIES = [
    (DepartmentRepositoryImpl, DepartmentRepository),
    (EmployeeRepositoryImpl, EmployeeRepository),

]

class DomainAdaptersProvider(Provider):
    """Domain adapter provider."""

    scope = Scope.REQUEST

    for impl, interface in REPOSITORIES:
        locals()[f"{interface.__name__.lower()}"] = provide(
            impl, provides=interface, scope=Scope.REQUEST
        )
