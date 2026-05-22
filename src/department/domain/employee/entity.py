from datetime import date, datetime

from department.domain.common.entitiy import Entity
from department.domain.department.value_objects import DepartmentId
from department.domain.employee.value_object import EmployeeId, EmployeeName, Position


class Employee(Entity[EmployeeId]):
    def __init__(
            self,
            employee_id: EmployeeId,
            department_id: DepartmentId,
            full_name: EmployeeName,
            position: Position,
            hired_at: date | None,
            created_at: datetime
    ) -> None:
        super().__init__(employee_id)
        self._department_id = department_id
        self._full_name = full_name
        self._position = position
        self._hired_at = hired_at
        self._created_at = created_at

    @property
    def department_id(self) -> DepartmentId:
        return self._department_id

    @property
    def full_name_vo(self) -> EmployeeName:
        return self._full_name

    @property
    def position(self) -> Position:
        return self._position

    @property
    def hired_at(self) -> date | None:
        return self._hired_at

    @property
    def created_at(self) -> datetime:
        return self._created_at
