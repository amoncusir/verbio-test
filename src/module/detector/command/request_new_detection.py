from dataclasses import dataclass

from src.module.common.command import Command, CommandRequest, CommandResponse
from src.module.common.domain.command_executor import CommandExecutor
from src.module.detector.command.execute_detection_algorithm import (
    ExecuteDetectionAlgorithmCommand,
    ExecuteDetectionAlgorithmCommandRequest,
)
from src.module.detector.domain.text_detection.repository import TextDetectionRepository, TextDetectionIDGenerator
from src.module.detector.domain.text_detection.text_detection import TextDetection
from src.module.detector.domain.value_objects import Language
from src.module.detector.types import TextDetectionIDType


class RequestNewDetectionCommandRequest(CommandRequest):
    language: Language
    text_content: str
    algorithm_name: str
    strict_detection: bool = False


class RequestNewDetectionCommandResponse(CommandResponse):
    detection_id: TextDetectionIDType


@dataclass(frozen=True)
class RequestNewDetectionCommand(Command[RequestNewDetectionCommandRequest, RequestNewDetectionCommandResponse]):

    command_executor: CommandExecutor
    text_detection_repository: TextDetectionRepository
    text_detection_id_generator: TextDetectionIDGenerator

    @classmethod
    def get_request_type(cls) -> type[RequestNewDetectionCommandRequest]:
        return RequestNewDetectionCommandRequest

    @classmethod
    def get_response_type(cls) -> type[RequestNewDetectionCommandResponse]:
        return RequestNewDetectionCommandResponse

    async def _execute(self, request: RequestNewDetectionCommandRequest) -> RequestNewDetectionCommandResponse:

        detection = await TextDetection.create(self.text_detection_id_generator, request.language, request.text_content)

        detection.strict = request.strict_detection

        await self.text_detection_repository.create(detection)

        await self.command_executor.execute_async(
            ExecuteDetectionAlgorithmCommand,
            ExecuteDetectionAlgorithmCommandRequest(
                detection_id=detection.id,
                algorithm=request.algorithm_name,
            ),
        )

        return RequestNewDetectionCommandResponse(detection_id=detection.id)
