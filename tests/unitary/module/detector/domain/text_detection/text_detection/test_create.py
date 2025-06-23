from unittest.mock import Mock

import pytest

from src.module.detector.domain.text_detection.repository import TextDetectionIDGenerator
from src.module.detector.domain.text_detection.status import DetectionStatus
from src.module.detector.domain.text_detection.text_detection import TextDetection, TextDetectionID
from src.module.detector.domain.value_objects import Language


@pytest.mark.asyncio
async def test_create():
    # Arrange
    id_generator = Mock(spec=TextDetectionIDGenerator)
    id_generator.generate.return_value = TextDetectionID('00000000-0000-0000-0000-000000000000')
    language = Language('en')
    content = "content to detect"

    # Act
    td: TextDetection = await TextDetection.create(id_generator, language, content)

    # Assert
    assert td.language == language
    assert td.content == content
    assert td.id == '00000000-0000-0000-0000-000000000000'

    assert td.status == DetectionStatus.PENDING

    assert not td.is_executed
    assert td.matches is None


@pytest.mark.asyncio
async def test_create_empty_language():
    # Arrange
    id_generator = Mock(spec=TextDetectionIDGenerator)
    id_generator.generate.return_value = TextDetectionID('00000000-0000-0000-0000-000000000000')
    language = None
    content = "content to detect"

    # Act & Assert
    with pytest.raises(ValueError):
        await TextDetection.create(id_generator, language, content)


@pytest.mark.asyncio
async def test_create_empty_content():
    # Arrange
    id_generator = Mock(spec=TextDetectionIDGenerator)
    id_generator.generate.return_value = TextDetectionID('00000000-0000-0000-0000-000000000000')
    language = Language('en')
    content = None

    # Act & Assert
    with pytest.raises(ValueError):
        await TextDetection.create(id_generator, language, content)
