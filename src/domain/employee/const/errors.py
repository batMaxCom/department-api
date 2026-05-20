from typing import Final
from domain.department.const import validation

# Employee Name
EMPTY_EMPLOYEE_NAME: Final[str] = "Employee name cannot be empty."
INVALID_EMPLOYEE_NAME_TYPE: Final[str] = "Employee name must be a string."
INVALID_EMPLOYEE_NAME_LENGTH: Final[str] = (
    f"Employee name must be between {validation.MIN_LENGTH} and {validation.MAX_LENGTH} characters."
)
INVALID_EMPLOYEE_NAME_FORMAT: Final[str] = "Employee name does not comply with the recording standard."

# Position
EMPTY_POSITION: Final[str] = "Employee name cannot be empty."
INVALID_POSITION_TYPE: Final[str] = "Employee name must be a string."
INVALID_POSITION_LENGTH: Final[str] = (
    f"Employee name must be between {validation.MIN_LENGTH} and {validation.MAX_LENGTH} characters."
)
INVALID_POSITION_FORMAT: Final[str] = "Employee name does not comply with the recording standard."
