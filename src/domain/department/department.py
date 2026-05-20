from datetime import datetime

from domain.common.entitiy import Entity
from domain.department.value_objects.department_id import DepartmentId
from domain.department.value_objects.department_name import DepartmentName


class Department(Entity[DepartmentId]):
    def __init__(
        self,
        department_id: DepartmentId,
        name: DepartmentName,
        parent_id: DepartmentId | None,
        created_at: datetime
    ) -> None:
        super().__init__(department_id)
        self._name = name
        self._parent_id = parent_id
        self._created_at = created_at

    @property
    def name_vo(self) -> DepartmentName:
        return self._name

    @property
    def parent_id(self) -> DepartmentId | None:
        return self._parent_id

    @property
    def created_at(self) -> datetime:
        return self._created_at
