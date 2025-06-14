from abc import abstractmethod
from typing import TYPE_CHECKING

from src.module.common.domain.repository import Repository, RepositoryError

if TYPE_CHECKING:
    from src.module.detector.domain.text_detection.text_detection import TextDetection, TextDetectionID


class TextDetectionNotFound(RepositoryError):
    pass


class TextDetectionIDGenerator:

    @abstractmethod
    async def generate(self) -> 'TextDetectionID': ...


class TextDetectionRepository(Repository):

    @abstractmethod
    async def create(self, text_detection: 'TextDetection'): ...

    @abstractmethod
    async def get_by_id(self, text_detection_id: 'TextDetectionID') -> 'TextDetection': ...

    @abstractmethod
    async def update_execute(self, text_detection: 'TextDetection'): ...

    @abstractmethod
    async def delete_by_id(self, text_detection_id: 'TextDetectionID'): ...
