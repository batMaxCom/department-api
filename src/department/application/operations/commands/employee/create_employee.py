from dataclasses import dataclass
from datetime import date

from department.application.common.dto import EmployeeDto
from department.application.ports.cqrs import CommandHandler, Command
from department.application.ports import IntegerIdGenerator, TimeProvider, AsyncTransactionManager
from department.domain.department.value_objects import DepartmentId
from department.domain.employee.entity import Employee
from department.domain.employee.repository import EmployeeRepository
from department.domain.employee.value_object import EmployeeId, EmployeeName, Position


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
        time_provider: TimeProvider,
        transaction_manager: AsyncTransactionManager
    ) -> None:
        self.__integer_id_generator = integer_id_generator
        self.__employee_repository = employee_repository
        self.__time_provider = time_provider
        self.__transaction_manager = transaction_manager

    async def handle(self, command: CreateEmployeeCommand) -> EmployeeDto:
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
        return EmployeeDto.from_entity(employee)
