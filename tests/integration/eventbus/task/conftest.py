from unittest.mock import Mock

from src.module.common.command import Command, CommandRequest, CommandResponse


class MockRequest(CommandRequest):
    name: str
    number: int
    list_value: list[str]
    default_value: str = "default"
    none_value: object = None


class MockResponse(CommandResponse):
    pass


class MockCommand(Command[MockRequest, MockResponse]):

    mock_execute = Mock(return_value=MockResponse())

    @classmethod
    def get_request_type(cls) -> type[MockRequest]:
        return MockRequest

    @classmethod
    def get_response_type(cls) -> type[MockResponse]:
        return MockResponse

    async def _execute(self, request: MockRequest) -> MockResponse:
        return self.mock_execute(request)
