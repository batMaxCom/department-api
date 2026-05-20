from dataclasses import dataclass, field
from enum import Enum, auto

from domain.common.const import errors as text


class DomainTypeError(Enum):
    VALIDATION = auto()
    DOMAIN = auto()
    FORBIDDEN = auto()
    CONFLICT = auto()


@dataclass(frozen=True, slots=True)
class DomainError(Exception):
    type: DomainTypeError = field(default=DomainTypeError.VALIDATION)
    message: str = field(default=text.VALIDATION_ERROR)
