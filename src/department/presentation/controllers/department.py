from datetime import date
from typing import Annotated, Literal

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body, Query
from starlette import status

from department.application.common.dto import (
    DepartmentDetailsDto,
    DepartmentDto,
    EmployeeDto,
)
from department.application.operations.commands.department import (
    CreateDepartmentCommand,
    UpdateDepartmentCommand,
    DeleteDepartmentCommand,
)
from department.application.operations.commands.employee import CreateEmployeeCommand
from department.application.operations.queries.department import GetDepartmentQuery
from department.application.ports.cqrs import Sender as MediatR

DEPARTMENT_ROUTER = APIRouter(prefix="/departments", tags=["Department"])


@DEPARTMENT_ROUTER.post(
    "",
    summary="Create a new department",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_department(
    name: Annotated[str, Body(embed=True)],
    parent_id: Annotated[int | None, Body(embed=True)] = None,
    *,
    mediatr: FromDishka[MediatR]
) -> DepartmentDto:
    command = CreateDepartmentCommand(
        name=name,
        parent_id=parent_id
    )
    return await mediatr.send(command)

@DEPARTMENT_ROUTER.get(
    "/{department_id}",
    summary="Get department details by ID",
    status_code=status.HTTP_200_OK,
)
@inject
async def get_department(
    department_id: int,
    depth: Annotated[int, Query()] = 1,
    include_employees: Annotated[bool, Query()] = True,
    *,
    mediatr: FromDishka[MediatR]
) -> DepartmentDetailsDto:
    query = GetDepartmentQuery(
        department_id=department_id,
        include_employees=include_employees,
        depth=depth
    )
    result = await mediatr.send(query)
    return result


@DEPARTMENT_ROUTER.patch(
    "/{department_id}",
    summary="Update an existing department",
    status_code=status.HTTP_200_OK
)
@inject
async def update_department(
    department_id: int,
    name: Annotated[str | None, Body(embed=True)],
    parent_id: Annotated[int | None, Body(embed=True)],
    *,
    mediatr: FromDishka[MediatR]
) -> DepartmentDto:
    command = UpdateDepartmentCommand(
        department_id=department_id,
        name=name,
        parent_id=parent_id
    )
    result = await mediatr.send(command)
    return result

@DEPARTMENT_ROUTER.delete(
    "/{department_id}",
    summary="Delete a department (cascade or reassign)",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_department(
    department_id: int,
    mode: Annotated[Literal["cascade", "reassign"], Body(embed=True)],
    reassign_to_department_id: Annotated[int, Body(embed=True)],
    *,
    mediatr: FromDishka[MediatR],
) -> None:
    command = DeleteDepartmentCommand(
        department_id=department_id,
        mode=mode,
        reassign_to_department_id=reassign_to_department_id
    )
    await mediatr.send(command)


@DEPARTMENT_ROUTER.post(
    "/{department_id}/employees/",
    summary="Create an employee in a department",
    status_code=status.HTTP_200_OK,
)
@inject
async def create_employee(
    department_id: int,
    full_name: Annotated[str, Body(embed=True)],
    position: Annotated[str, Body(embed=True)],
    hired_at: Annotated[date | None, Body(embed=True)],
    *,
    mediatr: FromDishka[MediatR],
) -> EmployeeDto:
    command = CreateEmployeeCommand(
        department_id=department_id,
        full_name=full_name,
        position=position,
        hired_at=hired_at
    )
    result = await mediatr.send(command)
    return result
