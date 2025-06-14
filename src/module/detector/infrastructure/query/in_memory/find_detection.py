from dataclasses import dataclass
from typing import Optional

from src.module.detector.infrastructure.repository.in_memory.text_detection import InMemoryTextDetectionRepository
from src.module.detector.query import FindTextDetectionQuery, FindTextDetectionQueryRequest
from src.module.detector.query.projections import TextDetectionProjection


@dataclass
class InMemoryRepositoryFindTextDetectionQuery(FindTextDetectionQuery):

    in_memory_repository: InMemoryTextDetectionRepository

    async def _execute(self, request: FindTextDetectionQueryRequest) -> Optional[TextDetectionProjection]:
        store = self.in_memory_repository.dump()
        value = store.get(request.detection_id)

        if not value:
            return None

        return TextDetectionProjection(
            id=value.id,
            status=value.status,
            language=value.language,
            content=value.content,
            matches=value.matches,
            has_detections=len(value.matches) > 0 if value.matches else None,
        )
