from contextlib import asynccontextmanager
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from dependency_injector.containers import Container
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.rabbitmq import RabbitMqContainer

from src.config.app import AppConfig
from src.module.common.domain.command_executor import CommandExecutor
from tests.integration.eventbus.test_container import EventBusContainer


@pytest.fixture(scope="session")
def testcontainer_rabbitmq() -> RabbitMqContainer:
    with RabbitMqContainer(image="rabbitmq:4", username="test", password="test") as container:
        wait_for_logs(container, "Server startup complete", timeout=60)
        yield container


@pytest.fixture(scope="session")
def rabbitmq_url(testcontainer_rabbitmq) -> str:
    rabbit_params = testcontainer_rabbitmq.get_connection_params()

    username = rabbit_params.credentials.username
    password = rabbit_params.credentials.password
    host = rabbit_params.host
    port = rabbit_params.port
    vhost = rabbit_params.virtual_host

    return f"amqp://{username}:{password}@{host}:{port}/{vhost}"


@pytest.fixture
def app_config():
    return AppConfig(name="integration.eventbus", version="0.0.0-testing", profiles=["test"], debug=True)


@pytest.fixture
def faststream_config(rabbitmq_url):
    config = {
        "rabbitmq": {
            "url": rabbitmq_url,
            "max_consumers": 1,
            "graceful_timeout": 30,
            "event": {
                "exchange_name": "event",
                "auto_delete": True,
            },
            "task": {
                "exchange_name": "task",
                "route_key": "service_integration",
            },
        }
    }

    print("RabbitMQ Config:", config)
    return config


@pytest.fixture(scope="function", autouse=True)
def container(faststream_config, app_config):

    container = EventBusContainer(
        app_config=app_config,
    )

    container.config.from_dict(faststream_config)

    return container


@pytest_asyncio.fixture
async def init_manager(container):

    @asynccontextmanager
    async def wrapper() -> AsyncGenerator[Container, None]:
        await container.init_resources()
        try:
            yield container
        finally:
            await container.shutdown_resources()

    return wrapper


@pytest.fixture(scope="function")
def faststream(container):
    return container.faststream


@pytest.fixture
def command_executor(faststream) -> CommandExecutor:
    return faststream.rabbit_task_executor()
