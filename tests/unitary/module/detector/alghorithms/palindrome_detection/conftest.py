import pytest

from src.module.detector.alghorithms.palindrom_detection import PalindromeDetectionAlgorithm
from src.module.detector.domain.text_detection_algorithm import TextDetectionAlgorithm


@pytest.fixture
def algorithm() -> TextDetectionAlgorithm:
    return PalindromeDetectionAlgorithm()
