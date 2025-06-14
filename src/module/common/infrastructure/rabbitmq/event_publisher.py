from dataclasses import dataclass
from logging import getLogger
from typing import Any, Awaitable

from dependency_injector.providers import Callable

from src.module.common.domain.event_publisher import EventPublisher
from src.module.common.domain.events import DomainEvent

_logger = getLogger(__name__)


@dataclass(frozen=True)
class RabbitMQEventPublisher(EventPublisher):
    _publisher: Callable[[str, Any], Awaitable]

    async def publish(self, event: DomainEvent):
        event_dict = event.to_dict()
        routing_key = event.routing_path()
        _logger.debug(
            "Publishing event[%s] ID: %s routing_key: %s body: %s",
            event.__class__.__name__,
            event.id,
            routing_key,
            event_dict,
        )

        await self._publisher(routing_key=routing_key, msg=event_dict)
