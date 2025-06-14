from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Projection(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    created_at: datetime = Field(default_factory=datetime.now)
