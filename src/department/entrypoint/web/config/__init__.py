from .db import PostgresConfig
from .web import WebConfig, get_web_config
from .app import AppConfig


__all__ = (
    "AppConfig",
    "PostgresConfig",
    "WebConfig",
    "get_web_config",
)
