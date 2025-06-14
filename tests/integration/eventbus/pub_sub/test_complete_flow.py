from unittest.mock import MagicMock

import pytest
from dependency_injector import providers
from faststream.rabbit import RabbitBroker

from src.app.rabbitmq import rabbit_subscriber
from tests.helpers import run_until_success


@pytest.fixture(scope="function", autouse=True)
def mocked_handler(faststream):

    mock = MagicMock(name='mock_handler')

    @rabbit_subscriber(name="test.mock", routing_key="test.*")
    async def mocked_subs(msg):
        mock(msg)

    faststream.event_rabbit_subscribers.override(
        providers.Factory(
            list,
            [mocked_subs()],
        )
    )

    return mock


@pytest.fixture(scope="function")
def broker(faststream, mocked_handler) -> RabbitBroker:
    return faststream.broker()


@pytest.fixture(scope="function")
def publisher(faststream, mocked_handler):
    return faststream.publisher()


@pytest.mark.asyncio
async def test_publish_event_is_received_by_subscriber_same_arguments(init_manager, publisher, broker, mocked_handler):

    async def assert_subscriber_event():
        mocked_handler.assert_called_once_with({"key": "value"})

    async with init_manager():
        await publisher(msg={"key": "value"}, routing_key="test.catch")
        await run_until_success(assert_subscriber_event, timeout=10)
