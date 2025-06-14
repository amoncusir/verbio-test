from dataclasses import dataclass
from typing import Callable, Coroutine, Any, Optional


@dataclass(frozen=True, kw_only=True)
class FastRabbitHandler:
    callable: Callable[..., Coroutine[Any, Any, Any]]
    routing_key: str
    name: str
    args: dict

    @property
    def dlq_name(self) -> str:
        return f"{self.name}.dlq"


def rabbit_subscriber(
    routing_key: str,
    name: Optional[str] = None,
    title: Optional[str] = None,
    **extra_args,
):
    def wrapper(func: Callable[..., Coroutine[Any, Any, Any]]):
        def factory(*args, **kwargs):
            f_title = title or func.__qualname__
            f_name = name or func.__qualname__
            return FastRabbitHandler(
                callable=func,
                routing_key=routing_key,
                name=f_name,
                args={'title': f_title, 'description': func.__doc__, **extra_args},
            )

        return factory

    return wrapper
