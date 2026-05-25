from dataclasses import dataclass
from datetime import date

from department.application.common.application_error import ApplicationError, ApplicationTypeError
from department.application.common.dto import EmployeeDto
from department.application.ports.cqrs import CommandHandler, Command
from department.application.ports import IntegerIdGenerator, TimeProvider, AsyncTransactionManager, Logger
from department.domain.department.repository import DepartmentRepository
from department.domain.department.value_objects import DepartmentId
from department.domain.employee.entity import Employee
from department.domain.employee.repository import EmployeeRepository
from department.domain.employee.value_object import EmployeeId, EmployeeName, Position
from department.application.common.const import errors as error_text


@dataclass(frozen=True, slots=True)
class CreateEmployeeCommand(Command[EmployeeDto]):
    department_id: int
    full_name: str
    position: str
    hired_at: date | None

class CreateEmployeeCommandHandler(CommandHandler[CreateEmployeeCommand, EmployeeDto]):
    def __init__(
        self,
        integer_id_generator: IntegerIdGenerator,
        employee_repository: EmployeeRepository,
        department_repository: DepartmentRepository,
        time_provider: TimeProvider,
        transaction_manager: AsyncTransactionManager,
        logger: Logger,
    ) -> None:
        self.__integer_id_generator = integer_id_generator
        self.__employee_repository = employee_repository
        self.__department_repository = department_repository
        self.__time_provider = time_provider
        self.__transaction_manager = transaction_manager
        self.__logger = logger

    async def handle(self, command: CreateEmployeeCommand) -> EmployeeDto:
        department_id = DepartmentId(command.department_id)
        if not await self.__department_repository.exists(id=department_id):
            raise ApplicationError(
                type=ApplicationTypeError.NOT_FOUND,
                message=error_text.DEPARTMENT_NOT_FOUND
            )
        employee = Employee(
            employee_id=EmployeeId(await self.__integer_id_generator.next_id()),
            department_id=DepartmentId(command.department_id),
            full_name=EmployeeName(command.full_name),
            position=Position(command.position),
            hired_at=command.hired_at,
            created_at=self.__time_provider.current_time(),
        )
        await self.__employee_repository.add(employee)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            "Employee created",
            employee_id=str(employee.entity_id),
            department_id=command.department_id,
            full_name=command.full_name,
        )
        return EmployeeDto.from_entity(employee)
