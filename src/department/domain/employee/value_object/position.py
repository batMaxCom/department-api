import re
from dataclasses import dataclass

from department.domain.common.domain_errors import DomainError, DomainTypeError
from department.domain.common.value_object import ValueObject

from department.domain.employee.const import errors as error_text
from department.domain.employee.const.validation import position as validation


@dataclass(frozen=True, slots=True)
class Position(ValueObject):
    value: str

    def _validate(self) -> None:
        if self.value is None:
            raise DomainError(type=DomainTypeError.VALIDATION, message=error_text.EMPTY_POSITION)
        if not isinstance(self.value, str):
            raise DomainError(
                type=DomainTypeError.VALIDATION, message=error_text.INVALID_POSITION_TYPE
            )
        if not (validation.MIN_LENGTH <= len(self.value) <= validation.MAX_LENGTH):
            raise DomainError(
                type=DomainTypeError.VALIDATION, message=error_text.INVALID_POSITION_LENGTH
            )
        if not re.match(validation.REGEX, self.value):
            raise DomainError(
                type=DomainTypeError.VALIDATION, message=error_text.INVALID_POSITION_FORMAT
            )
