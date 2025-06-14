from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.module.common.domain.rules import Rule, RuleError

if TYPE_CHECKING:
    from src.module.detector.domain.text_detection.text_detection import TextDetection


@dataclass(frozen=True)
class DetectionRule(ABC, Rule):
    detection: 'TextDetection'


@dataclass(frozen=True)
class IsDetectionAllowedToExecuteRule(DetectionRule):

    def __call__(self):
        if self.detection.is_executed:
            # Could be a more specific exception, but is ok for the test
            raise RuleError(f'Detection {self.detection} is already executed')


@dataclass(frozen=True)
class UpdateStrictValueRule(DetectionRule):

    def __call__(self):
        if self.detection.is_executed:
            # Could be a more specific exception, but is ok for the test
            raise RuleError(f"Can not update strict value of detection {self.detection} after execution")
