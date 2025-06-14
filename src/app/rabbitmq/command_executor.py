import logging
from dataclasses import dataclass
from typing import Type, Annotated

from faststream.rabbit import RabbitBroker, RabbitExchange
from faststream.rabbit.message import RabbitMessage
from faststream.utils.context.types import Context

from src.app.dependency import DependencyManager
from src.app.rabbitmq.settings import RabbitMQTaskSettings
from src.config.app import AppConfig
from src.module.common.command import Command, CommandRequest
from src.module.common.domain.command_executor import CommandExecutor

_logger = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class Task:  # Convert to namedtuple
    command_reference: str
    request: dict


@dataclass(frozen=True)
class RabbitMQCommandExecutor(CommandExecutor):

    app_config: AppConfig
    settings: RabbitMQTaskSettings
    dependency_manager: DependencyManager
    broker: RabbitBroker
    exchange: RabbitExchange

    async def execute_async(self, command: Type[Command], request: CommandRequest):
        if not isinstance(request, command.get_request_type()):
            raise ValueError("Invalid request type")

        command_reference = self.dependency_manager.find_command_reference(command)

        task = self.build_task(command_reference, request)
        await self.publish_task(task)

    async def publish_task(self, task: Task):
        _logger.info("Publishing task %s", task)

        result = await self.broker.publish(
            task.request,
            routing_key=self.settings.route_key,
            message_type=task.command_reference,
            exchange=self.exchange,
            mandatory=True,
            persist=True,
            headers={
                "x-project-name": self.app_config.name,
                "x-project-version": self.app_config.version,
            },
        )

        _logger.debug("Published task %s with result %s", task, result)
        return result

    def build_task(self, command_reference: str, request: CommandRequest) -> Task:
        return Task(
            command_reference=command_reference,
            request=request.model_dump(),
        )


@dataclass(frozen=True)
class RabbitMQCommandExecutorTaskHandler:
    dependency_manager: DependencyManager

    async def process_event(self, data: dict, message: Annotated[RabbitMessage, Context()]):
        _logger.info("Processing task %s", message)

        task = Task(
            command_reference=message.raw_message.type,
            request=data,
        )

        await self.process_task(task)

    async def process_task(self, task: Task):
        command, request = self.get_command(task)

        await command(request)

    def get_command(self, task: Task) -> (Command, CommandRequest):
        command_provider = self.dependency_manager.find_command_by_ref(task.command_reference)
        command = command_provider()
        request_type = command.get_request_type()
        request = request_type(**task.request)

        return command, request
