from dataclasses import dataclass

from src.module.common.command import Command, CommandRequest, CommandResponse
from src.module.detector.domain.text_detection.repository import TextDetectionRepository
from src.module.detector.types import TextDetectionIDType


class DeleteDetectionCommandRequest(CommandRequest):
    detection_id: TextDetectionIDType


class DeleteDetectionCommandResponse(CommandResponse):
    pass


@dataclass(frozen=True)
class DeleteDetectionCommand(Command[DeleteDetectionCommandRequest, DeleteDetectionCommandResponse]):
    text_detection_repository: TextDetectionRepository

    @classmethod
    def get_request_type(cls) -> type[DeleteDetectionCommandRequest]:
        return DeleteDetectionCommandRequest

    @classmethod
    def get_response_type(cls) -> type[DeleteDetectionCommandResponse]:
        return DeleteDetectionCommandResponse

    async def _execute(self, request: DeleteDetectionCommandRequest) -> DeleteDetectionCommandResponse:
        await self.text_detection_repository.delete_by_id(request.detection_id)
        return DeleteDetectionCommandResponse()
