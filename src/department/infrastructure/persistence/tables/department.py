from sqlalchemy import BIGINT, Column, Table, String, DateTime
from sqlalchemy.orm import composite

from department.domain.department.entity import Department
from department.domain.department.value_objects import DepartmentName
from department.infrastructure.persistence.tables.base import MAPPER_REGISTRY

DEPARTMENT_TABLE = Table(
    "departments",
    MAPPER_REGISTRY.metadata,
    Column("id", BIGINT, primary_key=True, autoincrement=False),
    Column("name", String, nullable=False),
    Column("parent_id", BIGINT, nullable=False),
    Column("created_at", DateTime, nullable=False),
)

def map_department_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        Department,
        DEPARTMENT_TABLE,
        properties={
            "_entity_id": DEPARTMENT_TABLE.c.id,
            "_name": composite(DepartmentName, DEPARTMENT_TABLE.c.name),
            "_parent_id": DEPARTMENT_TABLE.c.parent_id,
            "_created_at": DEPARTMENT_TABLE.c.created_at,
        }
    )
