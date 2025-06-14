from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.config.app import AppConfig
from src.module.common.infrastructure.rabbitmq.event_publisher import RabbitMQEventPublisher
from src.module.common.presentation.http import build_router
from src.module.providers import RouteProvider


class CommonContainer(DeclarativeContainer):
    config = providers.Configuration()
    app_config = providers.Dependency(AppConfig)
    publisher = providers.Dependency()

    event_publisher = providers.Factory(
        RabbitMQEventPublisher,
        _publisher=publisher,
    )

    routes = RouteProvider(
        build_router,
        app_config=app_config,
    )
