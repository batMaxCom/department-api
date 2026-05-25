from typing import Final

# Department
DEPARTMENT_NOT_FOUND: Final[str] = "Department not found."
DEPARTMENTS_EXIST: Final[str] = "Department already exists in this parent."
DEPARTMENT_REASSIGN_SELF_FORBIDDEN: Final[str] = (
    "Department cannot be reassigned to its own descendant."
)
DEPARTMENT_CIRCULAR_DEPENDENCY: Final[str] = "Department cycle detected"
DEPARTMENT_REASSIGN_ID_REQUIRED: Final[str] = (
    "reassign_to_department_id is required when mode='reassign'."
)
DEPARTMENT_DELETE_MODE_INVALID: Final[str] = (
    "Unknown delete mode. Use 'cascade' or 'reassign'."
)
DEPARTMENT_REASSIGN_TO_DESCENDANT_FORBIDDEN: Final[str] = (
    "Department cannot be reassigned to its own descendant."
)