from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    """Response class for query results."""
    status_code: int

@dataclass(frozen=True)
class ErrorResponse(Response):
    error: str
