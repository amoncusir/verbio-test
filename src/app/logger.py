import logging
import sys
from logging import Formatter, Handler

from src.config.app import AppConfig


def build_formatter() -> Formatter:
    formatter = Formatter("[%(asctime)s] [%(process)d][%(taskName)s] %(levelname)s:\t%(name)s --- %(message)s")
    return formatter


def build_handler() -> Handler:

    handler = logging.StreamHandler(sys.stdout)
    formatter = build_formatter()
    handler.setFormatter(formatter)

    return handler


def configure_logger(log_level: str | int, root_name: str = "src"):
    handler = build_handler()

    project_logger = logging.getLogger(root_name)
    project_logger.setLevel(log_level)
    project_logger.addHandler(handler)
    project_logger.propagate = False

    return project_logger


def print_app_config(app: AppConfig):
    _logger = logging.getLogger("src.app")

    _logger.info(
        "App Config - Name: %s; Version: %s, Profiles: %s, Debug: %s, Log Level: %s",
        app.name,
        app.version,
        app.profiles,
        app.debug,
        app.log_level,
    )
