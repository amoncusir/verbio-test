from abc import ABC
from typing import Optional

from src.module.common.query import QueryRequest, Query
from src.module.detector.query.projections import TextDetectionProjection
from src.module.detector.types import TextDetectionIDType


class FindTextDetectionQueryRequest(QueryRequest):
    detection_id: TextDetectionIDType


class FindTextDetectionQuery(ABC, Query[FindTextDetectionQueryRequest, Optional[TextDetectionProjection]]):

    @classmethod
    def get_request_type(cls) -> type[FindTextDetectionQueryRequest]:
        return FindTextDetectionQueryRequest

    @classmethod
    def get_response_type(cls) -> type[Optional[TextDetectionProjection]]:
        return Optional[TextDetectionProjection]
