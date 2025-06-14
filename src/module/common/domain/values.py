from abc import ABC, abstractmethod
from datetime import datetime, UTC
from typing import Self


class DateTime(datetime):

    @classmethod
    # pylint: disable=W0221
    def now(cls) -> Self:
        return super(DateTime, cls).now(UTC)

    @classmethod
    def from_datetime(cls, dt: datetime) -> Self:
        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, tzinfo=dt.tzinfo)


class Serializable(ABC):
    @abstractmethod
    def to_dict(self) -> dict: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> Self: ...
