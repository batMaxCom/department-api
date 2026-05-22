from dishka import Provider, Scope, provide_all

from department.application.operations.commands.department import (
    CreateDepartmentCommandHandler,
    DeleteDepartmentCommandHandler,
    UpdateDepartmentCommandHandler
)
from department.application.operations.commands.employee import  CreateEmployeeCommandHandler
from department.application.operations.queries.department import GetDepartmentQueryHandler

COMMAND_HANDLERS = [
    # Department
    CreateDepartmentCommandHandler,
    UpdateDepartmentCommandHandler,
    DeleteDepartmentCommandHandler,
    # Employee
    CreateEmployeeCommandHandler,
]

QUERY_HANDLERS = [
    # Department
    GetDepartmentQueryHandler,
]


class HandlersProvider(Provider):
    """HTTP handlers"""

    # HTTP
    scope = Scope.REQUEST

    command_handlers = provide_all(*COMMAND_HANDLERS)
    query_handlers = provide_all(*QUERY_HANDLERS)
