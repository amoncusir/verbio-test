from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.module.detector.query.projections import TextDetectionProjection


class TextDetectionDto(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    status: str
    language: str
    content: str
    matches: Optional[list[str]] = None
    has_detections: Optional[bool] = None

    @classmethod
    def from_projection(cls, projection: TextDetectionProjection):
        return cls(
            id=projection.id,
            status=str(projection.status),
            language=str(projection.language),
            content=projection.content,
            matches=projection.matches,
            has_detections=projection.has_detections,
        )
