import logging
from abc import abstractmethod
from datetime import datetime

from pydantic import BaseModel, ConfigDict

_logger = logging.getLogger(__name__)


class CommandRequest(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)


class CommandResponse(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)


class Command[Request: CommandRequest, Response: CommandResponse]:

    @classmethod
    @abstractmethod
    def get_request_type(cls) -> type[Request]:
        """
        Returns the request type
        """

    @classmethod
    @abstractmethod
    def get_response_type(cls) -> type[Response]:
        """
        Returns the response type
        """

    if _logger.isEnabledFor(logging.DEBUG):

        async def __call__(self, request: Request) -> Response:

            start = datetime.now()

            _logger.debug("Execute Command[%s] with %s", self.__class__.__name__, request)

            result = await self._execute(request)

            _logger.debug(
                "Finish Command[%s] on time {%s} with %s", self.__class__.__name__, datetime.now() - start, result
            )

            return result

    else:

        async def __call__(self, request: Request) -> Response:
            return await self._execute(request)

    @abstractmethod
    async def _execute(self, request: Request) -> Response:
        """
        Implements the Command Logic. DO NOT CALL THIS METHOD DIRECTLY.
        """
