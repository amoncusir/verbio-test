import logging
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from fastapi import APIRouter, Depends

from src.app import Application, get_app
from src.module.detector.alghorithms.palindrom_detection import PalindromeDetectionAlgorithm
from src.module.detector.command import RequestNewDetectionCommand, RequestNewDetectionCommandRequest
from src.module.detector.domain.value_objects import Language

router = APIRouter(prefix="/detection/text", tags=["detection", "text"])

logger = logging.getLogger(__name__)


class DetectPalindromeRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    text_content: str
    language: str = Field(min_length=2, max_length=2, pattern="^[a-z]{2}$")


@router.post("/palindrome", tags=["palindrome"])
async def detect_palindrome(
    app: Annotated[Application, Depends(get_app)],
    body: DetectPalindromeRequest,
    strict: bool = False,
):
    request = RequestNewDetectionCommandRequest(
        strict_detection=strict,
        language=Language.from_part_one(body.language),
        text_content=body.text_content,
        algorithm_name=PalindromeDetectionAlgorithm.name(),
    )

    command = app.find_command(RequestNewDetectionCommand)

    return await command(request)
