import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.module.common.domain.events import DomainEvent


class EventPublisher(ABC):

    @abstractmethod
    async def publish(self, event: 'DomainEvent'): ...

    async def publish_all(self, events: list['DomainEvent']):
        async with asyncio.TaskGroup() as tg:
            for event in events:
                tg.create_task(self.publish(event))
