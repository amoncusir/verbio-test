from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.module.common.domain.command_executor import CommandExecutor
from src.module.detector.alghorithms.palindrom_detection import PalindromeDetectionAlgorithm
from src.module.detector.command import (
    DeleteDetectionCommand,
    ExecuteDetectionAlgorithmCommand,
    RequestNewDetectionCommand,
)
from src.module.detector.domain.text_detection.repository import TextDetectionRepository, TextDetectionIDGenerator
from src.module.detector.domain.text_detection_algorithm import TextDetectionAlgorithmFactory
from src.module.detector.infrastructure.query.in_memory.find_detection import InMemoryRepositoryFindTextDetectionQuery
from src.module.detector.infrastructure.query.in_memory.search_detections import (
    InMemoryRepositorySearchTextDetectionsQuery,
)
from src.module.detector.infrastructure.repository.in_memory.text_detection import (
    InMemoryTextDetectionRepository,
    UUIDTextDetectionIDGenerator,
)
from src.module.detector.presentation.http import build_router
from src.module.providers import RouteProvider, CommandProvider, QueryProvider


class InMemoryPersistenceContainer(DeclarativeContainer):

    uuid_text_detection_id_generator = providers.Factory(UUIDTextDetectionIDGenerator)

    text_detection_repository = providers.Singleton(
        InMemoryTextDetectionRepository,
    )

    find_text_detection_query = QueryProvider(
        InMemoryRepositoryFindTextDetectionQuery,
        in_memory_repository=text_detection_repository,
    )

    search_text_detections_query = QueryProvider(
        InMemoryRepositorySearchTextDetectionsQuery,
        in_memory_repository=text_detection_repository,
    )


class AlgorithmsContainer(DeclarativeContainer):
    palindrome_text_detection_algorithm = providers.Singleton(
        PalindromeDetectionAlgorithm,
    )

    factory = providers.Factory(
        TextDetectionAlgorithmFactory,
        providers.List(
            palindrome_text_detection_algorithm,
        ),
    )


class CommandsContainer(DeclarativeContainer):
    text_detection_id_generator = providers.Dependency(TextDetectionIDGenerator)
    text_detection_repository = providers.Dependency(TextDetectionRepository)
    algorithm_factory = providers.Dependency(TextDetectionAlgorithmFactory)
    command_executor = providers.Dependency(CommandExecutor)

    request_new_detection = CommandProvider(
        RequestNewDetectionCommand,
        command_executor=command_executor,
        text_detection_repository=text_detection_repository,
        text_detection_id_generator=text_detection_id_generator,
    )

    execute_detection = CommandProvider(
        ExecuteDetectionAlgorithmCommand,
        text_detection_repository=text_detection_repository,
        algorithm_factory=algorithm_factory,
    ).with_reference("execute_detection")

    delete = CommandProvider(
        DeleteDetectionCommand,
        text_detection_repository=text_detection_repository,
    )


class DetectorContainer(DeclarativeContainer):
    config = providers.Configuration()

    command_executor = providers.Dependency(CommandExecutor)

    in_memory_storage = providers.Container(
        InMemoryPersistenceContainer,
    )

    algorithms = providers.Container(
        AlgorithmsContainer,
    )

    commands = providers.Container(
        CommandsContainer,
        text_detection_id_generator=in_memory_storage.uuid_text_detection_id_generator,
        text_detection_repository=in_memory_storage.text_detection_repository,
        algorithm_factory=algorithms.factory,
        command_executor=command_executor,
    )

    routes = RouteProvider(
        build_router,
    )


__all__ = ["DetectorContainer"]
