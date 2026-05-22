from typing import Any

from department.application.operations.queries.department import (
    GetDepartmentQuery,
    GetDepartmentQueryHandler,
)
from department.application.ports.cqrs import RequestHandler, BaseRequest
from department.infrastructure.mediator import Registry

QUERY_HANDLERS: list[tuple[type[BaseRequest[Any]], type[RequestHandler[Any, Any]]]] = [
    # Department
    (GetDepartmentQuery, GetDepartmentQueryHandler),
]


def register_queries(registry: Registry) -> None:
    for query, handler in QUERY_HANDLERS:
        registry.add_request_handler(query, handler)
