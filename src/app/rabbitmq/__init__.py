from typing import Protocol, Any

from .subscriber import rabbit_subscriber


class RabbitPublisher(Protocol):

    def __call__(self, routing_key: str, msg: Any, **kwargs): ...


__all__ = [
    'rabbit_subscriber',
    'RabbitPublisher',
]
