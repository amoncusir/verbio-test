from abc import ABC
from datetime import datetime
from typing import Optional

from src.module.common.projection import Projection
from src.module.common.query import QueryRequest, Query
from src.module.detector.domain.value_objects import Language
from src.module.detector.query.projections import TextDetectionProjection


class SearchTextDetectionsQueryRequest(QueryRequest):
    by_language: Optional[Language] = None
    by_range: Optional[tuple[datetime, datetime]] = None
    index: int = 0
    limit: int = 50


class SearchTextDetections(Projection):
    values: list[TextDetectionProjection]


class SearchTextDetectionsQuery(ABC, Query[SearchTextDetectionsQueryRequest, SearchTextDetections]):

    @classmethod
    def get_request_type(cls) -> type[SearchTextDetectionsQueryRequest]:
        return SearchTextDetectionsQueryRequest

    @classmethod
    def get_response_type(cls) -> type[SearchTextDetections]:
        return SearchTextDetections
