from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.dependency import DependencyManager
from src.app.rabbitmq.container import FastStreamContainer


class EventBusContainer(DeclarativeContainer):
    config = providers.Configuration()

    app_config = providers.Dependency()

    __self__ = providers.Self()

    dependency_manager = providers.Factory(
        DependencyManager,
        container=__self__,
    )

    faststream = providers.Container(
        FastStreamContainer,
        config=config,
        app_config=app_config,
        root_container=__self__,
        dependency_manager=dependency_manager,
    )
