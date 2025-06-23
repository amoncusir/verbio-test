from unittest.mock import Mock

import pytest

from src.module.detector.domain.text_detection.repository import TextDetectionIDGenerator
from src.module.detector.domain.text_detection.text_detection import TextDetection, TextDetectionID
from src.module.detector.domain.value_objects import Language


@pytest.fixture
def text_detection_builder():

    async def builder(text: str, lang: str) -> TextDetection:
        id_generator = Mock(spec=TextDetectionIDGenerator)
        id_generator.generate.return_value = TextDetectionID('00000000-0000-0000-0000-000000000000')
        language = Language(lang)

        return await TextDetection.create(id_generator, language, text)

    return builder
