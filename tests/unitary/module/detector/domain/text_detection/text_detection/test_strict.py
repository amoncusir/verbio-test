from unittest.mock import AsyncMock

import pytest

from src.module.common.domain.rules import RuleError
from src.module.detector.domain.text_detection_algorithm import TextDetectionAlgorithm


@pytest.mark.asyncio
async def test_raise_if_modify_strictness_in_executed_text_detection(text_detection_builder):
    # Arrange
    algorithm = AsyncMock(spec=TextDetectionAlgorithm)
    algorithm.execute_detection.return_value = []

    td = await text_detection_builder('my_content', 'en')
    td.strict = False

    # Act
    await td.execute_detection(algorithm)

    # Assert
    with pytest.raises(RuleError):
        td.strict = True

    assert td.strict is False
