from dataclasses import dataclass
from typing import Self

from department.domain.employee.entity import Employee


@dataclass(slots=True)
class EmployeeDto:
    id: int
    full_name: str

    @classmethod
    def from_entity(cls, entity: Employee) -> Self:
        return cls(
            id=entity.entity_id,
            full_name=entity.full_name_vo.value,
        )
