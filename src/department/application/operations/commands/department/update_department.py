from dataclasses import dataclass

from department.application.common.dto import DepartmentDto
from department.application.ports.cqrs import CommandHandler, Command
from department.application.ports import AsyncTransactionManager
from department.domain.department.repository import DepartmentRepository
from department.domain.department.value_objects import DepartmentId, DepartmentName


@dataclass(frozen=True, slots=True)
class UpdateDepartmentCommand(Command[DepartmentDto]):
    department_id: int
    name: str | None
    parent_id: int | None

class UpdateDepartmentCommandHandler(CommandHandler[UpdateDepartmentCommand, DepartmentDto]):
    def __init__(
        self,
        department_repository: DepartmentRepository,
        transaction_manager: AsyncTransactionManager

    ) -> None:
        self.__department_repository = department_repository
        self.__transaction_manager = transaction_manager



    async def handle(self, command: UpdateDepartmentCommand) -> DepartmentDto:
        department_id = DepartmentId(command.department_id)
        department = await self.__department_repository.get(id=department_id)

        if command.parent_id:
            department.change_parent(DepartmentId(command.parent_id))
        if command.name:
            department.rename(DepartmentName(command.name))
        await self.__department_repository.update(department)
        await self.__transaction_manager.commit()
        return DepartmentDto.from_entity(department)
