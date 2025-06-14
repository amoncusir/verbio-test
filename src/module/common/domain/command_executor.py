from abc import ABC, abstractmethod
from typing import Type

from src.module.common.command import Command, CommandRequest


class CommandExecutor(ABC):

    @abstractmethod
    async def execute_async(self, command: Type[Command], request: CommandRequest): ...
