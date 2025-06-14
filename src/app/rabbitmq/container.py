from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.dependency import DependencyManager
from src.app.rabbitmq.fast_stream import (
    build_event_exchange,
    build_event_rabbit_router,
    build_rabbitmq_broker,
    build_fast_stream,
    fast_stream_initializer,
    rabbit_publisher,
    build_task_exchange,
    build_task_rabbit_queue,
    build_task_rabbit_router,
)
from src.app.rabbitmq.command_executor import RabbitMQCommandExecutorTaskHandler, RabbitMQCommandExecutor
from src.app.utils import find_providers
from src.config.app import AppConfig
from src.app.rabbitmq.settings import RabbitMQSettings
from src.module.providers import SubscriberProvider


class FastStreamContainer(DeclarativeContainer):
    config = providers.Configuration()

    app_config = providers.Dependency(AppConfig)
    root_container = providers.Dependency()
    dependency_manager = providers.Dependency(DependencyManager)

    settings = providers.Factory(RabbitMQSettings.from_dict, config.rabbitmq)

    # CommandManager ###################################################################################################

    rabbit_task_manager = providers.Resource(
        RabbitMQCommandExecutorTaskHandler,
        dependency_manager=dependency_manager,
    )

    # Event ############################################################################################################

    event_settings = settings.provided.event

    event_exchange = providers.Singleton(
        build_event_exchange,
        settings=event_settings,
    )

    event_rabbit_subscribers = providers.Factory(
        find_providers,
        root_container,
        SubscriberProvider,
    )

    event_router = providers.Singleton(
        build_event_rabbit_router,
        settings=event_settings,
        exchange=event_exchange,
        subscribers=event_rabbit_subscribers,
    )

    # Task #############################################################################################################

    task_settings = settings.provided.task

    task_exchange = providers.Singleton(
        build_task_exchange,
        settings=task_settings,
    )

    task_queue = providers.Singleton(
        build_task_rabbit_queue,
        settings=task_settings,
    )

    task_router = providers.Singleton(
        build_task_rabbit_router,
        settings=task_settings,
        queue=task_queue,
        exchange=task_exchange,
        handler=rabbit_task_manager.provided.process_event,
    )

    # FastStream #######################################################################################################

    broker = providers.Singleton(
        build_rabbitmq_broker,
        app_config=app_config,
        rabbitmq_settings=settings,
        event_router=event_router,
        task_router=task_router,
    )

    app = providers.Singleton(
        build_fast_stream,
        settings=settings,
        broker=broker,
        subscribers=event_rabbit_subscribers,
    )

    initializer = providers.Resource(
        fast_stream_initializer,
        app=app,
        app_config=app_config,
    )

    # Publisher ########################################################################################################

    rabbit_task_executor = providers.Singleton(
        RabbitMQCommandExecutor,
        app_config=app_config,
        settings=task_settings,
        dependency_manager=dependency_manager,
        broker=broker,
        exchange=task_exchange,
    )

    publisher = providers.Factory(
        rabbit_publisher,
        broker=broker,
        exchange=event_exchange,
    )
