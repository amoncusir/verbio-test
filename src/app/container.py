from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.dependency import DependencyManager
from src.app.fast_api import build_fastapi, build_router
from src.app.logger import configure_logger, print_app_config
from src.app.rabbitmq.container import FastStreamContainer
from src.app.utils import find_providers
from src.config.api import ApiSettings
from src.config.app import AppConfig
from src.module.container import ModuleContainer
from src.module.providers import RouteProvider


class MainContainer(DeclarativeContainer):
    config = providers.Configuration()

    __self__ = providers.Self()

    app_config = providers.Factory(AppConfig.from_dict, config)

    logger = providers.Resource(
        configure_logger,
        log_level=app_config.provided.log_level,
    )

    faststream_logger = providers.Resource(
        configure_logger,
        log_level=app_config.provided.log_level,
        root_name="faststream",
    )

    print_info = providers.Resource(
        print_app_config,
        app_config,
    )

    api_settings = providers.Factory(
        ApiSettings.from_dict,
        config.api,
    )

    dependency_manager = providers.Factory(
        DependencyManager,
        __self__,
    )

    faststream = providers.Container(
        FastStreamContainer,
        config=config.faststream,
        app_config=app_config,
        root_container=__self__,
        dependency_manager=dependency_manager,
    )

    module_container = providers.Container(
        ModuleContainer,
        config=config.module,
        publisher=faststream.publisher,
        command_executor=faststream.rabbit_task_executor,
        app_config=app_config,
    )

    fastapi = providers.Singleton(
        build_fastapi,
        router=providers.Singleton(
            build_router,
            providers.Factory(find_providers, __self__, RouteProvider),
        ),
        api_settings=api_settings,
        app_config=app_config,
    )
