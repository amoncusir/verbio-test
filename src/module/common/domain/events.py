from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Self
from uuid import uuid4, UUID

from dacite import from_dict

from src.module.common.domain.values import Serializable, DateTime


@dataclass(frozen=True, kw_only=True)
class DomainEvent(Serializable):
    id: UUID = field(default_factory=uuid4)
    event_created_at: DateTime = field(default_factory=DateTime.now)

    @classmethod
    @abstractmethod
    def routing_path(cls) -> str: ...

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "event_created_at": self.event_created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return from_dict(
            cls,
            {
                **data,
                "id": UUID(data["id"]),
                "event_created_at": DateTime.fromisoformat(data["event_created_at"]),
            },
        )
