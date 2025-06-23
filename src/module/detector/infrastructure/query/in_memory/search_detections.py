from dataclasses import dataclass

from src.module.detector.domain.text_detection.text_detection import TextDetection
from src.module.detector.infrastructure.repository.in_memory.text_detection import InMemoryTextDetectionRepository
from src.module.detector.query import (
    SearchTextDetectionsQuery,
    SearchTextDetectionsQueryRequest,
    SearchTextDetections,
    TextDetectionProjection,
)


@dataclass
class InMemoryRepositorySearchTextDetectionsQuery(SearchTextDetectionsQuery):
    in_memory_repository: InMemoryTextDetectionRepository

    async def _execute(self, request: SearchTextDetectionsQueryRequest) -> SearchTextDetections:
        store = self.in_memory_repository.dump()

        def v_filter(v: TextDetection):
            if request.by_language and v.language != request.by_language:
                return False

            if request.by_range and not (request.by_range[0] <= v.created_at <= request.by_range[1]):
                return False

            return True

        def v_map(v: TextDetection) -> TextDetectionProjection:
            return TextDetectionProjection(
                id=v.id,
                status=v.status,
                language=v.language,
                content=v.content,
                matches=v.matches,
                has_detections=len(v.matches) > 0 if v.matches is not None else None,
            )

        values = list(store.values())[request.index :]
        filtered_values = []

        for value in (v_map(v) for v in values if v_filter(v)):
            filtered_values.append(value)
            if len(filtered_values) >= request.limit:
                break

        return SearchTextDetections(values=list(filtered_values))
