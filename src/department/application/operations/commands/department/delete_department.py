from dataclasses import dataclass

from department.application.common.application_error import ApplicationError, ApplicationTypeError
from department.application.ports.cqrs import CommandHandler, Command
from department.application.ports import AsyncTransactionManager
from department.domain.department.repository import DepartmentRepository
from department.domain.department.value_objects import DepartmentId
from department.application.common.const.errors import DEPARTMENT_NOT_FOUND

@dataclass(frozen=True, slots=True)
class DeleteDepartmentCommand(Command[None]):
    department_id: int
    mode: str
    reassign_to_department_id: int


class DeleteDepartmentCommandHandler(CommandHandler[DeleteDepartmentCommand, None]):
    def __init__(
        self,
        department_repository: DepartmentRepository,
        transaction_manager: AsyncTransactionManager

    ) -> None:
        self.__department_repository = department_repository
        self.__transaction_manager = transaction_manager

    async def handle(self, command: DeleteDepartmentCommand) -> None:
        department_id = DepartmentId(command.department_id)
        department = await self.__department_repository.get(id=department_id)
        if department is None:
            raise ApplicationError(
                type=ApplicationTypeError.NOT_FOUND,
                message=DEPARTMENT_NOT_FOUND
            )
        await self.__department_repository.delete(department)
        await self.__transaction_manager.commit()
