from sqlalchemy import BIGINT, Column, Table, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import composite

from department.domain.employee.entity import Employee
from department.domain.employee.value_object import EmployeeName, Position
from department.infrastructure.persistence.tables.base import MAPPER_REGISTRY

EMPLOYEE_TABLE = Table(
    "employees",
    MAPPER_REGISTRY.metadata,
    Column("id", BIGINT, primary_key=True, autoincrement=False),
    Column("department_id", BIGINT, ForeignKey("departments.id"), nullable=False, index=True),
    Column("full_name", String, nullable=False),
    Column("position", String, nullable=False),
    Column("hired_at", Date, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

def map_employee_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        Employee,
        EMPLOYEE_TABLE,
        properties={
            "_entity_id": EMPLOYEE_TABLE.c.id,
            "_department_id": EMPLOYEE_TABLE.c.department_id,
            "_full_name": composite(EmployeeName, EMPLOYEE_TABLE.c.full_name),
            "_position": composite(Position, EMPLOYEE_TABLE.c.position),
            "_hired_at": EMPLOYEE_TABLE.c.hired_at,
            "_created_at": EMPLOYEE_TABLE.c.created_at
        },
    )
