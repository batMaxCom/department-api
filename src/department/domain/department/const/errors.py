from typing import Final
from department.domain.department.const import validation

EMPTY_DEPARTMENT_NAME: Final[str] = "Department name cannot be empty."
INVALID_DEPARTMENT_NAME_TYPE: Final[str] = "Department name must be a string."
INVALID_DEPARTMENT_NAME_LENGTH: Final[str] = (
    f"Department name must be between {validation.MIN_LENGTH} and {validation.MAX_LENGTH} characters."
)
INVALID_DEPARTMENT_NAME_FORMAT: Final[str] = "Department name does not comply with the recording standard."
