import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from src.app import Application, get_app
from src.module.detector.command.delete_detection import DeleteDetectionCommand, DeleteDetectionCommandRequest
from src.module.detector.domain.text_detection.text_detection import TextDetectionID
from src.module.detector.presentation.http.text_detection.dto import TextDetectionDto
from src.module.detector.query.find_detection import FindTextDetectionQuery, FindTextDetectionQueryRequest

router = APIRouter(prefix="/detection", tags=["detection"])

logger = logging.getLogger(__name__)


@router.get("/{detection_id}")
async def find_detection(app: Annotated[Application, Depends(get_app)], detection_id: str) -> TextDetectionDto:
    request = FindTextDetectionQueryRequest(detection_id=TextDetectionID(detection_id))

    query = app.find_query(FindTextDetectionQuery)

    projection = await query(request)

    return TextDetectionDto.from_projection(projection)


@router.delete("/{detection_id}", status_code=204)
async def delete_detection(app: Annotated[Application, Depends(get_app)], detection_id: str):
    request = DeleteDetectionCommandRequest(detection_id=TextDetectionID(detection_id))

    command = app.find_command(DeleteDetectionCommand)

    await command(request)
