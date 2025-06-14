import copy
from dataclasses import dataclass, field
from logging import getLogger
from typing import List, Self

from src.module.common.domain.entities import DomainEntity
from src.module.common.domain.event_publisher import EventPublisher
from src.module.common.domain.events import DomainEvent

logger = getLogger(__name__)


@dataclass(kw_only=True)
class AggregateRoot[ID](DomainEntity[ID]):

    __events_queue: List[DomainEvent] = field(default_factory=list, init=False, repr=False, compare=False, hash=False)

    def copy(self):
        model: Self = copy.deepcopy(self)
        model.__pop_events()  # pylint: disable=protected-access
        return model

    def __del__(self):
        if len(self.__events_queue) > 0:
            class_name = self.__class__.__qualname__
            logger.error("Remaining events on %s when destructor called! :: %s", class_name, self.__events_queue)

    def _add_event(self, event: DomainEvent):
        self.__events_queue.append(event)

    async def flush_events(self, publisher: EventPublisher):
        events = self.__pop_events()
        await publisher.publish_all(events)

    def __pop_events(self) -> List[DomainEvent]:
        flushed_events = self.__events_queue.copy()
        self.__events_queue.clear()
        return flushed_events

    def list_events_repr(self) -> List[str]:
        return [repr(e) for e in self.__events_queue]

    def read_events(self) -> List[DomainEvent]:
        return self.__events_queue.copy()
