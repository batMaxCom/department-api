from dishka import Provider, Scope, alias, provide
from sqlalchemy.ext.asyncio import AsyncSession

from department.application.ports.gateways import DepartmentGateway
from department.application.ports import IntegerIdGenerator, TimeProvider, AsyncTransactionManager
from department.infrastructure.adapters import IntegerIdGeneratorImpl, TimeProviderImpl
from department.infrastructure.persistence.adapters.gateways import DepartmentGatewayImpl

GATEWAYS = [
    (DepartmentGatewayImpl, DepartmentGateway),
]


class ApplicationAdaptersProvider(Provider):
    """Application adapter provider."""

    scope = Scope.REQUEST

    for impl, interface in GATEWAYS:
        locals()[f"{interface.__name__.lower()}"] = provide(impl, provides=interface)

    integer_id_generator = provide(IntegerIdGeneratorImpl, provides=IntegerIdGenerator)

    time_provider = provide(TimeProviderImpl, provides=TimeProvider)
    transaction_manager = alias(AsyncSession, provides=AsyncTransactionManager)
