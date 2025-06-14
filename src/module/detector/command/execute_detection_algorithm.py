from dataclasses import dataclass

from src.module.common.command import Command, CommandRequest, CommandResponse
from src.module.detector.domain.text_detection.repository import TextDetectionRepository
from src.module.detector.domain.text_detection_algorithm import TextDetectionAlgorithmFactory
from src.module.detector.types import TextDetectionIDType


class ExecuteDetectionAlgorithmCommandRequest(CommandRequest):
    detection_id: TextDetectionIDType
    algorithm: str


class ExecuteDetectionAlgorithmCommandResponse(CommandResponse):
    pass


@dataclass(frozen=True)
class ExecuteDetectionAlgorithmCommand(
    Command[ExecuteDetectionAlgorithmCommandRequest, ExecuteDetectionAlgorithmCommandResponse]
):
    text_detection_repository: TextDetectionRepository
    algorithm_factory: TextDetectionAlgorithmFactory

    @classmethod
    def get_request_type(cls) -> type[ExecuteDetectionAlgorithmCommandRequest]:
        return ExecuteDetectionAlgorithmCommandRequest

    @classmethod
    def get_response_type(cls) -> type[ExecuteDetectionAlgorithmCommandResponse]:
        return ExecuteDetectionAlgorithmCommandResponse

    async def _execute(
        self, request: ExecuteDetectionAlgorithmCommandRequest
    ) -> ExecuteDetectionAlgorithmCommandResponse:

        algorithm = self.algorithm_factory.build_by(algorithm_name=request.algorithm)
        detection = await self.text_detection_repository.get_by_id(request.detection_id)

        await detection.execute_detection(algorithm)

        await self.text_detection_repository.update_execute(detection)

        return ExecuteDetectionAlgorithmCommandResponse()
