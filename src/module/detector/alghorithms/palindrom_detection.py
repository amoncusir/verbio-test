from typing import Unpack
from unidecode import unidecode

from src.module.detector.domain.text_detection_algorithm import TextDetectionAlgorithm, TextDetectionParameters
from src.module.detector.domain.value_objects import Language


class PalindromeDetectionAlgorithm(TextDetectionAlgorithm):

    __name__ = "palindrome"

    punctuation_table: dict

    def __init__(self, punctuation_table: dict = None):
        self.punctuation_table = punctuation_table or str.maketrans("", "", ".,:;!¡¿?-_'")

    async def execute_detection(self, text: str, _: Language, **params: Unpack[TextDetectionParameters]) -> list[str]:
        params = self._default_parameters(params)
        transformed_text = text

        if params["ignore_case"]:
            transformed_text = transformed_text.lower()

        if params["ignore_spaces"]:
            transformed_text = transformed_text.replace(" ", "")

        if params["ignore_punctuation"]:
            transformed_text = transformed_text.translate(self.punctuation_table)

        if params["ignore_orthographic_symbols"]:
            transformed_text = unidecode(transformed_text)

        # Very simple palindrome detection
        return [text] if transformed_text == transformed_text[::-1] else []
