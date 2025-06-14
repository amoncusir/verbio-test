from abc import abstractmethod
from typing import TypedDict, Optional, Unpack, NotRequired

from src.module.detector.domain.value_objects import Language


class TextDetectionParameters(TypedDict):
    ignore_case: NotRequired[bool]
    ignore_spaces: NotRequired[bool]
    ignore_punctuation: NotRequired[bool]
    ignore_orthographic_symbols: NotRequired[bool]


class TextDetectionAlgorithm:

    __name__: str

    def _default_parameters(self, params: Optional[TextDetectionParameters]) -> TextDetectionParameters:
        return {
            "ignore_case": True,
            "ignore_spaces": True,
            "ignore_punctuation": True,
            "ignore_orthographic_symbols": True,
            **(params or {}),
        }

    @abstractmethod
    async def execute_detection(
        self, text: str, language: Language, **params: Unpack[TextDetectionParameters]
    ) -> list[str]: ...

    @classmethod
    def name(cls) -> str:
        return cls.__name__


class TextDetectionAlgorithmFactory:

    _algorithms: dict[str, TextDetectionAlgorithm] = {}

    def __init__(self, algorithms: list[TextDetectionAlgorithm]):
        for algorithm in algorithms:
            self._algorithms[algorithm.name()] = algorithm

    def build_by(self, *, algorithm_name: str) -> TextDetectionAlgorithm:
        return self._algorithms[algorithm_name]
