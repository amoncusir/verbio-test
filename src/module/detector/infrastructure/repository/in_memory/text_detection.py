from dataclasses import dataclass, field
from uuid import uuid4

from src.module.detector.domain.text_detection.repository import (
    TextDetectionRepository,
    TextDetectionNotFound,
    TextDetectionIDGenerator,
)
from src.module.detector.domain.text_detection.text_detection import TextDetection, TextDetectionID


class UUIDTextDetectionIDGenerator(TextDetectionIDGenerator):

    async def generate(self) -> TextDetectionID:
        return TextDetectionID(str(uuid4()))


@dataclass
class InMemoryTextDetectionRepository(TextDetectionRepository):

    _cache: dict[TextDetectionID, TextDetection] = field(default_factory=dict)

    def dump(self) -> dict[TextDetectionID, TextDetection]:
        return self._cache.copy()

    async def create(self, text_detection: TextDetection):
        self._cache[text_detection.id] = text_detection.copy()

    async def get_by_id(self, text_detection_id: TextDetectionID) -> TextDetection:
        value = self._cache.get(text_detection_id)

        if value is None:
            raise TextDetectionNotFound(f"Text detection with id {text_detection_id} not found")

        return value.copy()

    async def update_execute(self, text_detection: TextDetection):
        if text_detection.id not in self._cache:
            raise TextDetectionNotFound(f"Text detection with id {text_detection.id} not found to be updated.")

        self._cache[text_detection.id] = text_detection.copy()

    async def delete_by_id(self, text_detection_id: TextDetectionID):
        if text_detection_id not in self._cache:
            raise TextDetectionNotFound(f"Text detection with id {text_detection_id} not found to be deleted")

        del self._cache[text_detection_id]
