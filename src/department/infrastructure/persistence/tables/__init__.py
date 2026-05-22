from .base import METADATA, MAPPER_REGISTRY
from .employee import (
    EMPLOYEE_TABLE,
    map_employee_table,
)
from .setup import setup_mapping
from .department import (
    DEPARTMENT_TABLE,
    map_department_table,
)


__all__ = (
    "METADATA",
    "MAPPER_REGISTRY",
    "DEPARTMENT_TABLE",
    "EMPLOYEE_TABLE",
    "map_department_table",
    "map_employee_table",
    "setup_mapping",
)
