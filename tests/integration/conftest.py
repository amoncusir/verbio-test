import logging

import pytest

from src.app.logger import configure_logger


@pytest.fixture(autouse=True, scope="session")
def enable_test():
    configure_logger(logging.DEBUG, "test")
    configure_logger(logging.DEBUG, "src")
