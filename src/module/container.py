from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.config.app import AppConfig
from src.module.common.container import CommonContainer
from src.module.common.domain.command_executor import CommandExecutor
from src.module.detector import DetectorContainer


class ModuleContainer(DeclarativeContainer):
    config = providers.Configuration()
    publisher = providers.Dependency()
    command_executor = providers.Dependency(CommandExecutor)
    app_config = providers.Dependency(AppConfig)

    common_container = providers.Container(
        CommonContainer,
        config=config.common,
        app_config=app_config,
        publisher=publisher,
    )

    detector_container = providers.Container(
        DetectorContainer,
        config=config.detector,
        command_executor=command_executor,
    )
