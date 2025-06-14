from dataclasses import dataclass
from typing import Self, Optional

from src.module.common.domain.aggregates import AggregateRoot
from src.module.detector.domain.text_detection.repository import TextDetectionIDGenerator
from src.module.detector.domain.text_detection.rules import IsDetectionAllowedToExecuteRule, UpdateStrictValueRule
from src.module.detector.domain.text_detection.status import DetectionStatus
from src.module.detector.domain.text_detection_algorithm import TextDetectionAlgorithm
from src.module.detector.domain.value_objects import Language


class TextDetectionID(str):
    pass


@dataclass(kw_only=True)
class TextDetection(AggregateRoot[TextDetectionID]):
    _id: TextDetectionID
    _status: DetectionStatus = DetectionStatus.PENDING

    _language: Language
    _content: str
    _matches: Optional[list[str]] = None

    _strict: bool = False

    @classmethod
    async def create(cls, generator: TextDetectionIDGenerator, language: Language, content: str) -> Self:
        if not content:
            raise ValueError("Content cannot be empty.")

        if not language:
            raise ValueError("Language cannot be empty.")

        return cls(
            _id=await generator.generate(),
            _language=language,
            _content=content,
        )

    @property
    def status(self) -> DetectionStatus:
        return self._status

    @property
    def is_executed(self) -> bool:
        return self._status == DetectionStatus.EXECUTED

    @property
    def language(self) -> Language:
        return self._language

    @property
    def content(self) -> str:
        return self._content

    @property
    def matches(self) -> Optional[list[str]]:
        if self._matches is None:
            return None

        return self._matches.copy()

    @property
    def strict(self) -> bool:
        return self._strict

    @strict.setter
    def strict(self, value: bool):
        UpdateStrictValueRule.spark(detection=self)

        self._strict = value
        self._update()

    async def execute_detection(self, algorithm: TextDetectionAlgorithm):
        IsDetectionAllowedToExecuteRule.spark(detection=self)

        self._matches = await algorithm.execute_detection(
            self._content,
            self._language,
            ignore_case=not self._strict,
            ignore_spaces=not self._strict,
            ignore_punctuation=not self._strict,
            ignore_orthographic_symbols=not self._strict,
        )

        self._status = DetectionStatus.EXECUTED
        self._update()
