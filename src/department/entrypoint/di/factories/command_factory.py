from typing import Any

from department.application.operations.commands.department import (
    CreateDepartmentCommand,
    UpdateDepartmentCommand,
    DeleteDepartmentCommand,
    CreateDepartmentCommandHandler,
    UpdateDepartmentCommandHandler,
    DeleteDepartmentCommandHandler,
)
from department.application.operations.commands.employee import (
    CreateEmployeeCommand,
    CreateEmployeeCommandHandler,
)

from department.infrastructure.mediator.registry import Registry

from department.application.ports.cqrs import RequestHandler, BaseRequest

COMMAND_HANDLERS: list[tuple[type[BaseRequest[Any]], type[RequestHandler[Any, Any]]]] = [
    # Department
    (CreateDepartmentCommand, CreateDepartmentCommandHandler),
    (UpdateDepartmentCommand, UpdateDepartmentCommandHandler),
    (DeleteDepartmentCommand, DeleteDepartmentCommandHandler),
    # Employee
    (CreateEmployeeCommand, CreateEmployeeCommandHandler),
]

def register_commands(registry: Registry) -> None:
    for command, handler in COMMAND_HANDLERS:
        registry.add_request_handler(command, handler)
