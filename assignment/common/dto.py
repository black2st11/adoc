from datetime import datetime
from typing import Any

import orjson
from pydantic import ConfigDict, BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda dt: dt.isoformat()
        }
    )


class PaginationItem(BaseModel):
    items: list[Any]
    total: int
    page: int
    size: int
    total_page: int