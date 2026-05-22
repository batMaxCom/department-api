from dataclasses import dataclass
from typing import Self

from department.application.common.dto.employee import EmployeeDto
from department.domain.department.entity import Department


@dataclass(slots=True)
class DepartmentDto:
    id: str
    name: str
    parent_id: str | None

    @classmethod
    def from_entity(cls, entity: Department) -> Self:
        return cls(
            id=entity.entity_id.__str__(),
            name=entity.name_vo.value,
            parent_id=entity.parent_id.__str__()
        )

@dataclass(slots=True)
class DepartmentDetailsDto:
    department: DepartmentDto
    employees: list[EmployeeDto]
    children: list["DepartmentDetailsDto"]
