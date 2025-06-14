"""

Naming convention:

- *Settings: Allow only data changes. The behavior should be the same for all settings.
- *Config: Allow functional changes. Different configurations can provide different behaviors.

"""

from typing import Self, Optional

from pydantic import ConfigDict, BaseModel


class BaseProperties(BaseModel):
    model_config = ConfigDict(frozen=True)

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Self:
        if data is None:
            return cls()

        return cls(**data)
