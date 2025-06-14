from typing import Optional

from src.module.common.projection import Projection
from src.module.detector.domain.text_detection.status import DetectionStatus
from src.module.detector.domain.text_detection.text_detection import TextDetectionID
from src.module.detector.domain.value_objects import Language


class TextDetectionProjection(Projection):
    id: TextDetectionID
    status: DetectionStatus
    language: Language
    content: str
    matches: Optional[list[str]]
    has_detections: Optional[bool]
