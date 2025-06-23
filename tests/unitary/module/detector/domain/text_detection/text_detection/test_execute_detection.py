from unittest.mock import AsyncMock

import pytest

from src.module.detector.domain.text_detection.status import DetectionStatus
from src.module.detector.domain.text_detection_algorithm import TextDetectionAlgorithm
from src.module.detector.domain.value_objects import Language


@pytest.mark.asyncio
async def test_execute_empty_detection_not_strict(text_detection_builder):
    # Arrange
    algorithm = AsyncMock(spec=TextDetectionAlgorithm)
    algorithm.execute_detection.return_value = []

    td = await text_detection_builder('my_content', 'en')
    td.strict = False

    # Act
    await td.execute_detection(algorithm)

    # Assert
    assert td.is_executed
    assert td.status == DetectionStatus.EXECUTED
    assert td.matches == []

    algorithm.execute_detection.assert_called_with(
        'my_content',
        Language('en'),
        ignore_case=True,
        ignore_spaces=True,
        ignore_punctuation=True,
        ignore_orthographic_symbols=True,
    )


@pytest.mark.asyncio
async def test_execute_content_detection_not_strict(text_detection_builder):
    # Arrange
    algorithm = AsyncMock(spec=TextDetectionAlgorithm)
    algorithm.execute_detection.return_value = ['my_content']

    td = await text_detection_builder('my_content', 'en')
    td.strict = False

    # Act
    await td.execute_detection(algorithm)

    # Assert
    assert td.is_executed
    assert td.status == DetectionStatus.EXECUTED
    assert td.matches == ['my_content']

    algorithm.execute_detection.assert_called_with(
        'my_content',
        Language('en'),
        ignore_case=True,
        ignore_spaces=True,
        ignore_punctuation=True,
        ignore_orthographic_symbols=True,
    )


@pytest.mark.asyncio
async def test_execute_content_detection_strict(text_detection_builder):
    # Arrange
    algorithm = AsyncMock(spec=TextDetectionAlgorithm)
    algorithm.execute_detection.return_value = ['my_content']

    td = await text_detection_builder('my_content', 'en')
    td.strict = True

    # Act
    await td.execute_detection(algorithm)

    # Assert
    assert td.is_executed
    assert td.status == DetectionStatus.EXECUTED
    assert td.matches == ['my_content']

    algorithm.execute_detection.assert_called_with(
        'my_content',
        Language('en'),
        ignore_case=False,
        ignore_spaces=False,
        ignore_punctuation=False,
        ignore_orthographic_symbols=False,
    )
