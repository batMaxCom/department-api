from sqlalchemy import BIGINT, Column, Table, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import composite, relationship

from department.domain.department.entity import Department
from department.domain.department.value_objects import DepartmentName
from department.domain.employee.entity import Employee
from department.infrastructure.persistence.tables.base import MAPPER_REGISTRY

DEPARTMENT_TABLE = Table(
    "departments",
    MAPPER_REGISTRY.metadata,
    Column("id", BIGINT, primary_key=True, autoincrement=False),
    Column("name", String, nullable=False),
    Column("parent_id", BIGINT, ForeignKey("departments.id"), nullable=True, index=True),
    Column("created_at", DateTime(timezone=True), nullable=False),

    UniqueConstraint(
        "parent_id",
        "name",
        name="uq_department_parent_name"
    )
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
            "children": relationship(
                "Department",
                cascade="all, delete",
                back_populates="parent",
            ),
            "parent": relationship(
                "Department",
                remote_side=[DEPARTMENT_TABLE.c.id],
                back_populates="children",
            ),
            "employees": relationship(
                Employee,
                cascade="all, delete-orphan",
            ),
        }
    )
