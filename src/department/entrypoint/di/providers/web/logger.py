from typing import cast, NewType

import structlog
from dishka import Provider, Scope, alias, provide
from structlog.stdlib import BoundLogger

from department.application.ports import Logger

CQRSLogger = NewType("CQRSLogger", Logger)


class LoggerAdapterProvider(Provider):
    scope = Scope.APP

    @provide
    def bound_logger(self) -> BoundLogger:
        return cast(BoundLogger, structlog.get_logger())

    logger = alias(source=BoundLogger, provides=Logger)
