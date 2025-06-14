import logging
from abc import abstractmethod
from datetime import datetime

from pydantic import BaseModel, ConfigDict


_logger = logging.getLogger(__name__)


class QueryRequest(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)


class Query[Request: QueryRequest, Response]:

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

            _logger.debug("Execute Query[%s] with %s", self.__class__.__name__, request)

            result = await self._execute(request)

            _logger.debug(
                "Finish Query[%s] on time {%s} with %s", self.__class__.__name__, datetime.now() - start, result
            )

            return result

    else:

        async def __call__(self, request: Request) -> Response:
            return await self._execute(request)

    @abstractmethod
    async def _execute(self, request: Request) -> Response:
        """
        Implements the Query Logic. DO NOT CALL THIS METHOD DIRECTLY.
        """
