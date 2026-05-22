from dishka import AsyncContainer, make_async_container

from department.entrypoint.di.providers.web import (
    MediatorProvider,
    WebConfigProvider,
    WebPersistenceProvider,
    DomainAdaptersProvider,
    ApplicationAdaptersProvider,
    FastapiProvider,
    HandlersProvider,
)
from department.entrypoint.web.config import AppConfig, PostgresConfig


def web_container(
        app_config: AppConfig,
        db_config: PostgresConfig,
) -> AsyncContainer:
    return make_async_container(
        MediatorProvider(),
        WebConfigProvider(),
        WebPersistenceProvider(),
        DomainAdaptersProvider(),
        ApplicationAdaptersProvider(),
        FastapiProvider(),
        HandlersProvider(),
        context={
            AppConfig: app_config,
            PostgresConfig: db_config,
        }
    )
