from typing import Annotated

from pydantic import BeforeValidator

from src.module.detector.domain.text_detection.text_detection import TextDetectionID


TextDetectionIDType = Annotated[TextDetectionID, BeforeValidator(TextDetectionID)]
