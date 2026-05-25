from dataclasses import dataclass

from department.application.common.application_error import ApplicationError, ApplicationTypeError
from department.application.ports.cqrs import CommandHandler, Command
from department.application.ports import AsyncTransactionManager, Logger
from department.domain.department.repository import DepartmentRepository
from department.domain.department.value_objects import DepartmentId
from department.domain.employee.repository import EmployeeRepository
from department.application.common.const import errors as error_texts


@dataclass(frozen=True, slots=True)
class DeleteDepartmentCommand(Command[None]):
    department_id: int
    mode: str
    reassign_to_department_id: int | None = None


class DeleteDepartmentCommandHandler(
    CommandHandler[DeleteDepartmentCommand, None]
):
    def __init__(
        self,
        department_repository: DepartmentRepository,
        employee_repository: EmployeeRepository,
        transaction_manager: AsyncTransactionManager,
        logger: Logger,
    ) -> None:
        self.__department_repository = department_repository
        self.__employee_repository = employee_repository
        self.__transaction_manager = transaction_manager
        self.__logger = logger

    async def handle(self, command: DeleteDepartmentCommand) -> None:
        department_id = DepartmentId(command.department_id)

        if command.mode == "cascade":
            await self._cascade_delete(department_id)
            await self.__logger.ainfo(
                "Department cascade deleted",
                department_id=command.department_id,
            )
        elif command.mode == "reassign":
            if command.reassign_to_department_id is None:
                raise ApplicationError(
                    type=ApplicationTypeError.VALIDATION,
                    message=error_texts.DEPARTMENT_REASSIGN_ID_REQUIRED
                )

            target_id = DepartmentId(
                command.reassign_to_department_id
            )

            if target_id == department_id:
                raise ApplicationError(
                    type=ApplicationTypeError.VALIDATION,
                    message=error_texts.DEPARTMENT_REASSIGN_SELF_FORBIDDEN,
                )

            await self._reassign_delete(
                department_id=department_id,
                target_id=target_id,
            )
            await self.__logger.ainfo(
                "Department reassign deleted",
                department_id=command.department_id,
                reassign_to=command.reassign_to_department_id,
            )

        else:
            raise ApplicationError(
                type=ApplicationTypeError.VALIDATION,
                message=error_texts.DEPARTMENT_DELETE_MODE_INVALID,
            )

        await self.__transaction_manager.commit()

    async def _cascade_delete(
        self,
        department_id: DepartmentId,
    ) -> None:
        await self._delete_department(department_id)

    async def _reassign_delete(
        self,
        department_id: DepartmentId,
        target_id: DepartmentId,
    ) -> None:

        department = await self.__department_repository.get(
            id=department_id
        )

        is_descendant = (
            await self.__department_repository.is_descendant(
                ancestor_id=department_id,
                descendant_id=target_id,
            )
        )

        if is_descendant:
            raise ApplicationError(
                type=ApplicationTypeError.CONFLICT,
                message=error_texts.DEPARTMENT_REASSIGN_TO_DESCENDANT_FORBIDDEN,
            )

        await self.__employee_repository.reassign_to_department(
            from_id=department_id,
            to_id=target_id,
        )

        children_ids = (
            await self.__department_repository.get_children_ids(
                department_id
            )
        )

        for child_id in children_ids:

            child = await self.__department_repository.get(
                id=child_id
            )

            child.change_parent(
                department.parent_id
            )

            await self.__department_repository.update(
                child
            )

        await self._delete_department(
            department_id
        )

    async def _delete_department(
        self,
        department_id: DepartmentId,
    ) -> None:

        department = await self.__department_repository.get(
            id=department_id
        )

        await self.__department_repository.delete(
            department
        )
