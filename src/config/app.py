import logging

from src.config import BaseProperties


class AppConfig(BaseProperties):

    name: str
    version: str

    profiles: list[str]
    debug: bool = False
    log_level: str = "INFO"

    @property
    def int_log_level(self) -> int:
        return logging.getLevelNamesMapping().get(self.log_level, logging.INFO)

    def contains_profile(self, profile: str) -> bool:
        return profile in self.profiles
