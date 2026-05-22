import re
from dataclasses import dataclass

from department.domain.common.domain_errors import DomainError, DomainTypeError
from department.domain.common.value_object import ValueObject

from department.domain.employee.const import errors as error_text
from department.domain.employee.const.validation import employee_name as validation



@dataclass(frozen=True, slots=True)
class EmployeeName(ValueObject):
    value: str

    def _validate(self) -> None:
        if self.value is None:
            raise DomainError(type=DomainTypeError.VALIDATION, message=error_text.EMPTY_EMPLOYEE_NAME)
        if not isinstance(self.value, str):
            raise DomainError(
                type=DomainTypeError.VALIDATION, message=error_text.INVALID_EMPLOYEE_NAME_TYPE
            )
        if not (validation.MIN_LENGTH <= len(self.value) <= validation.MAX_LENGTH):
            raise DomainError(
                type=DomainTypeError.VALIDATION, message=error_text.INVALID_EMPLOYEE_NAME_LENGTH
            )
        if not re.match(validation.REGEX, self.value):
            raise DomainError(
                type=DomainTypeError.VALIDATION, message=error_text.INVALID_EMPLOYEE_NAME_FORMAT
            )
