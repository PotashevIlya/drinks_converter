from typing import Optional

from pydantic import BaseModel, Field


class ConvertationData(BaseModel):
    source_name: str = Field(..., max_length=50)
    source_ml: int = Field(..., gt=0)
    target_name: Optional[str] = Field(None, max_length=50)
