from department.infrastructure.persistence.tables.department import map_department_table
from department.infrastructure.persistence.tables.employee import map_employee_table


def setup_mapping() -> None:
    map_department_table()
    map_employee_table()
