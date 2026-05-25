from dataclasses import dataclass

from department.application.common.application_error import ApplicationError, ApplicationTypeError
from department.application.common.dto import DepartmentDto
from department.application.ports.cqrs import CommandHandler, Command
from department.application.ports import AsyncTransactionManager, Logger
from department.domain.department.repository import DepartmentRepository
from department.domain.department.value_objects import DepartmentId, DepartmentName
from department.application.common.const import errors as error_texts


@dataclass(frozen=True, slots=True)
class UpdateDepartmentCommand(Command[DepartmentDto]):
    department_id: int
    name: str | None
    parent_id: int | None

class UpdateDepartmentCommandHandler(CommandHandler[UpdateDepartmentCommand, DepartmentDto]):
    def __init__(
        self,
        department_repository: DepartmentRepository,
        transaction_manager: AsyncTransactionManager,
        logger: Logger,
    ) -> None:
        self.__department_repository = department_repository
        self.__transaction_manager = transaction_manager
        self.__logger = logger

    async def handle(self, command: UpdateDepartmentCommand) -> DepartmentDto:
        department_id = DepartmentId(command.department_id)
        department = await self.__department_repository.get(id=department_id)

        if command.parent_id is not None:
            new_parent_id = DepartmentId(command.parent_id)
            await self.__validate_parent(
                department_id=department_id,
                parent_id=new_parent_id
            )
            department.change_parent(new_parent_id)

        if command.name is not None:
            department.rename(
                DepartmentName(command.name)
            )

        await self.__department_repository.update(department)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            "Department updated",
            department_id=command.department_id,
            name=command.name,
            parent_id=command.parent_id,
        )
        return DepartmentDto.from_entity(department)

    async def __validate_parent(
            self,
            department_id: DepartmentId,
            parent_id: DepartmentId
    ) -> None:
        if department_id == parent_id:
            raise ApplicationError(
                type=ApplicationTypeError.CONFLICT,
                message=error_texts.DEPARTMENT_REASSIGN_SELF_FORBIDDEN
            )

        parent = await self.__department_repository.get(
            id=parent_id
        )

        current_parent_id = parent.parent_id

        while current_parent_id is not None:
            if current_parent_id == department_id:
                raise ApplicationError(
                    type=ApplicationTypeError.CONFLICT,
                    message=error_texts.DEPARTMENT_CIRCULAR_DEPENDENCY
                )
            current_parent = await self.__department_repository.get(
                id=current_parent_id
            )
            current_parent_id = current_parent.parent_id
