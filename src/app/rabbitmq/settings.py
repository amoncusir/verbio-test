from typing import Optional

from src.config import BaseProperties


class RabbitMQEventSettings(BaseProperties):
    exchange_name: str
    auto_delete: bool = True
    default_retries: int = 3

    @property
    def dead_letter_exchange_name(self) -> str:
        return f"{self.exchange_name}.dle"


class RabbitMQTaskSettings(RabbitMQEventSettings):

    route_key: str

    @property
    def dead_letter_route_key(self) -> str:
        return f"{self.route_key}.dle"


class RabbitMQSettings(BaseProperties):

    url: str

    max_consumers: Optional[int] = None
    graceful_timeout: Optional[float] = None
    connection_timeout: Optional[float] = None

    event: RabbitMQEventSettings
    task: RabbitMQTaskSettings

    security: bool = False
