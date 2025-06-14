from abc import abstractmethod
from dataclasses import dataclass
from typing import NoReturn, Optional

from src.module.common.domain.errors import DomainError


class RuleError(DomainError):
    pass


@dataclass(frozen=True, kw_only=True)
class Rule:

    @abstractmethod
    def __call__(self): ...

    @classmethod
    def spark(cls, **kwargs) -> Optional[NoReturn]:
        rule = cls(**kwargs)
        rule()

    @classmethod
    def check(cls, **kwargs) -> bool:
        rule = cls(**kwargs)
        try:
            rule()
            return True
        except RuleError:
            return False
