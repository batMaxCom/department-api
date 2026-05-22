from dataclasses import dataclass

from department.application.common.application_error import ApplicationError, ApplicationTypeError
from department.application.ports.cqrs import CommandHandler, Command
from department.application.ports import AsyncTransactionManager
from department.domain.department.repository import DepartmentRepository
from department.domain.department.value_objects import DepartmentId
from department.domain.employee.repository import EmployeeRepository


@dataclass(frozen=True, slots=True)
class DeleteDepartmentCommand(Command[None]):
    department_id: int
    mode: str
    reassign_to_department_id: int | None = None


class DeleteDepartmentCommandHandler(CommandHandler[DeleteDepartmentCommand, None]):
    def __init__(
        self,
        department_repository: DepartmentRepository,
        employee_repository: EmployeeRepository,
        transaction_manager: AsyncTransactionManager,

    ) -> None:
        self.__department_repository = department_repository
        self.__employee_repository = employee_repository
        self.__transaction_manager = transaction_manager

    async def handle(self, command: DeleteDepartmentCommand) -> None:
        department_id = DepartmentId(command.department_id)

        if command.mode == "cascade":
            await self._cascade_delete(department_id)
        elif command.mode == "reassign":
            if command.reassign_to_department_id is None:
                raise ApplicationError(
                    type=ApplicationTypeError.VALIDATION,
                    message="reassign_to_department_id is required when mode=reassign"
                )
            await self._reassign_delete(
                department_id,
                DepartmentId(command.reassign_to_department_id),
            )
        else:
            raise ApplicationError(
                type=ApplicationTypeError.VALIDATION,
                message=f"Unknown mode: {command.mode}. Use 'cascade' or 'reassign'."
            )

        await self.__transaction_manager.commit()

    async def _cascade_delete(self, department_id: DepartmentId) -> None:
        children = await self.__department_repository.get_children_ids(department_id)
        for child_id in children:
            await self._cascade_delete(child_id)

        await self.__employee_repository.delete_by_department(department_id)
        await self._delete_department(department_id)

    async def _reassign_delete(
        self,
        department_id: DepartmentId,
        target_id: DepartmentId,
    ) -> None:
        await self.__employee_repository.reassign_to_department(department_id, target_id)

        children = await self.__department_repository.get_children_ids(department_id)
        for child_id in children:
            await self._cascade_delete(child_id)

        await self._delete_department(department_id)

    async def _delete_department(self, department_id: DepartmentId) -> None:
        dept = await self.__department_repository.get(id=department_id)
        await self.__department_repository.delete(dept)
