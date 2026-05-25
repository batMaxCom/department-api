from datetime import date
from dataclasses import dataclass
from typing import Self

from department.domain.employee.entity import Employee


@dataclass(slots=True)
class EmployeeDto:
    id: str
    full_name: str
    position: str
    hired_at: date | None
    department_id: str

    @classmethod
    def from_entity(cls, entity: Employee) -> Self:
        return cls(
            id=entity.entity_id.__str__(),
            full_name=entity.full_name_vo.value,
            position=entity.position_vo.value,
            hired_at=entity.hired_at,
            department_id=entity.department_id.__str__()
        )
