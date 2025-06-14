from typing import Optional

from pydantic import Field

from src.config import BaseProperties


class ApiSettings(BaseProperties):

    root_path: Optional[str] = Field("")
