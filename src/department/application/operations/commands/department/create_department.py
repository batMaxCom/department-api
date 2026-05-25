from dataclasses import dataclass

from department.application.common.application_error import ApplicationError, ApplicationTypeError
from department.application.common.dto import DepartmentDto
from department.application.ports.cqrs import CommandHandler, Command

from department.application.ports import IntegerIdGenerator, TimeProvider, AsyncTransactionManager
from department.domain.department.entity import Department
from department.domain.department.repository import DepartmentRepository
from department.domain.department.value_objects import DepartmentId, DepartmentName
from department.application.common.const import errors as error_texts


@dataclass(frozen=True, slots=True)
class CreateDepartmentCommand(Command[DepartmentDto]):
    name: str
    parent_id: int | None


class CreateDepartmentCommandHandler(CommandHandler[CreateDepartmentCommand, DepartmentDto]):
    def __init__(
        self,
        integer_id_generator: IntegerIdGenerator,
        department_repository: DepartmentRepository,
        time_provider: TimeProvider,
        transaction_manager: AsyncTransactionManager
    ) -> None:
        self.__integer_id_generator = integer_id_generator
        self.__department_repository = department_repository
        self.__time_provider = time_provider
        self.__transaction_manager = transaction_manager


    async def handle(self, command: CreateDepartmentCommand) -> DepartmentDto:
        if command.parent_id and await self.__department_repository.exists(
            name=command.name,
            parent_id=command.parent_id
        ):
            raise ApplicationError(
                type=ApplicationTypeError.CONFLICT,
                message=error_texts.DEPARTMENTS_EXIST
            )


        department = Department(
            department_id=DepartmentId(await self.__integer_id_generator.next_id()),
            name=DepartmentName(command.name),
            parent_id=DepartmentId(command.parent_id) if command.parent_id else None,
            created_at=self.__time_provider.current_time(),
        )
        await self.__department_repository.add(department)
        await self.__transaction_manager.commit()
        return DepartmentDto.from_entity(department)
