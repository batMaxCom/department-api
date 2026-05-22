from dataclasses import dataclass
from typing import Self

from department.application.common.dto.employee import EmployeeDto
from department.domain.department.entity import Department


@dataclass(slots=True)
class DepartmentDto:
    id: int
    name: str
    parent_id: int | None

    @classmethod
    def from_entity(cls, entity: Department) -> Self:
        return cls(
            id=entity.entity_id,
            name=entity.name_vo.value,
            parent_id=entity.parent_id
        )

@dataclass(slots=True)
class DepartmentDetailsDto:
    department: DepartmentDto
    employees: list[EmployeeDto]
    children: list["DepartmentDetailsDto"]
