import re
from dataclasses import dataclass

from domain.common.domain_errors import DomainError, DomainTypeError
from domain.common.value_object import ValueObject

from domain.department.const import errors as error_text
from domain.department.const import validation



@dataclass(frozen=True, slots=True)
class DepartmentName(ValueObject):
    value: str

    def _validate(self) -> None:
        if self.value is None:
            raise DomainError(type=DomainTypeError.VALIDATION, message=error_text.EMPTY_DEPARTMENT_NAME)
        if not isinstance(self.value, str):
            raise DomainError(
                type=DomainTypeError.VALIDATION, message=error_text.INVALID_DEPARTMENT_NAME_TYPE
            )
        if not (validation.MIN_LENGTH <= len(self.value) <= validation.MAX_LENGTH):
            raise DomainError(
                type=DomainTypeError.VALIDATION, message=error_text.INVALID_DEPARTMENT_NAME_LENGTH
            )
        if not re.match(validation.REGEX, self.value):
            raise DomainError(
                type=DomainTypeError.VALIDATION, message=error_text.INVALID_DEPARTMENT_NAME_FORMAT
            )
