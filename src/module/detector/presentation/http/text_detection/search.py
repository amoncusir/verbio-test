from datetime import datetime
from typing import Optional, Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field, ConfigDict, model_validator, PastDatetime

from src.app import Application, get_app
from src.module.detector.domain.value_objects import Language
from src.module.detector.presentation.http.text_detection.dto import TextDetectionDto
from src.module.detector.presentation.http.utils import decode_token, generate_token
from src.module.detector.query.search_detections import SearchTextDetectionsQueryRequest, SearchTextDetectionsQuery

router = APIRouter(prefix="/search/detection", tags=["search"])


class SearchParameters(BaseModel):
    lang: Optional[str] = Field(None, min_length=2, max_length=2, pattern="^[a-z]{2}$")
    from_date: Optional[PastDatetime] = None
    to_date: Optional[PastDatetime] = None
    index: int = 0
    next_token: str = None

    @model_validator(mode="after")
    def validate_date(self):
        if self is None:
            return self

        if (1 if self.from_date else 0) + (1 if self.to_date else 0) == 1:
            raise ValueError("from_date and to_date must be both set or both unset.")

        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValueError("from_date must be less than to_date.")

        return self

    @model_validator(mode="after")
    def token_inflater(self):
        if self is None:
            return self

        if self.next_token:
            self.lang, self.from_date, self.to_date, self.index = decode_token(self.next_token)

        return self

    def generate_token(self, offset: int) -> Optional[str]:
        if offset == 0:
            return None
        return generate_token(self.lang, self.from_date, self.to_date, self.index + offset)

    @property
    def domain_language(self) -> Optional[Language]:
        return Language.from_part_one(self.lang) if self.lang else None

    @property
    def range(self) -> Optional[tuple[datetime, datetime]]:
        return (self.from_date, self.to_date) if self.from_date and self.to_date else None


class SearchResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    values: list[TextDetectionDto]
    next_token: Optional[str] = None


@router.get('')
async def search_detections(
    app: Annotated[Application, Depends(get_app)],
    params: Annotated[SearchParameters, Query()],
) -> SearchResult:
    limit = 10

    request = SearchTextDetectionsQueryRequest(
        by_language=params.domain_language,
        index=params.index,
        limit=limit,
    )

    query = app.find_query(SearchTextDetectionsQuery)

    results = await query(request)

    results_len = len(results.values)

    return SearchResult(
        values=[TextDetectionDto.from_projection(projection) for projection in results.values],
        next_token=params.generate_token(results_len) if results_len == limit else None,
    )
