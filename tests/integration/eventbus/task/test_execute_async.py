import pytest

from src.module.providers import CommandProvider
from tests.helpers import run_until_success
from tests.integration.eventbus.task.conftest import MockCommand, MockRequest


@pytest.fixture
def mock_command_provider():
    return CommandProvider(MockCommand).with_reference("mock_command")


@pytest.mark.asyncio
async def test_execute_async(container, init_manager, command_executor, mock_command_provider):

    container.mock_command = mock_command_provider
    command: MockCommand = mock_command_provider()

    request = MockRequest(
        name="Test",
        number=1,
        list_value=["a", "b", "c"],
        none_value=None,
    )

    async def assert_command_executed():
        command.mock_execute.assert_called_once_with(request)

    async with init_manager():
        await command_executor.execute_async(MockCommand, request)
        await run_until_success(assert_command_executed)
