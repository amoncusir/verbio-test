import logging
import os
import threading
from typing import Type, Protocol, Any, Iterator

from fastapi import FastAPI

from src.app.dependency import DependencyManager
from src.app.utils import Singleton
from src.module.common.domain.command_executor import CommandExecutor

logger = logging.getLogger(__name__)

_thread_lock = threading.Lock()


class ApplicationContainer(Protocol):

    config: Any
    logger: Any
    faststream: Any
    dependency_manager: Any
    fastapi: Any

    async def init_resources(self): ...

    async def shutdown_resources(self): ...

    def check_dependencies(self): ...

    def traverse[T](self, types: list[type[T]] = None) -> Iterator[T]: ...


class Application(metaclass=Singleton):

    container: ApplicationContainer

    @classmethod
    def remove_instance(cls):
        Singleton.remove_instance(cls)

    @classmethod
    def init_with_container(cls, container_class: type, config=None, config_path=None):
        if container_class is None:
            raise ValueError("Container class is required")

        if config is None:
            config = {}

        if config_path is None:
            config_path = os.environ.get("APP_CONFIGURATION_FILE", default="./config/development.yaml")

        print(f"Loaded configuration from: {config_path}")

        container = container_class()
        container.config.from_yaml(config_path, required=True)
        container.config.from_dict(config)
        return cls(container)

    def __init__(self, container: ApplicationContainer = None):
        if container is None:
            raise ValueError("Container is required")

        self.container = container
        self.container.logger.init()

        if self.container.config.debug():
            print(f"With configuration: {self.container.config()}")
            self.container.check_dependencies()

    @property
    def dependency_manager(self) -> DependencyManager:
        return self.container.dependency_manager()

    @property
    def task_executor(self) -> CommandExecutor:
        return self.container.faststream.rabbit_task_executor()

    async def init(self):
        with _thread_lock:
            logger.debug("Initializing application...")
            await self.container.init_resources()
            logger.debug("Application initialized.")

    async def shutdown(self):
        with _thread_lock:
            logger.debug("Shutting down application...")
            await self.container.shutdown_resources()
            logger.debug("Application shut down.")

    def fastapi(self, lifespan=None) -> FastAPI:
        return self.container.fastapi(lifespan=lifespan)

    def find_command[T](self, uc_type: Type[T]) -> T:
        return self.dependency_manager.find_command_by_type(uc_type)()

    def find_query[T](self, q_type: Type[T]) -> T:
        return self.dependency_manager.find_query_by_type(q_type)()
