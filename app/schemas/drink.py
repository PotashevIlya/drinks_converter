from typing import Optional

from pydantic import BaseModel, Field


class DrinkBase(BaseModel):
    name: str = Field(..., max_length=50)
    average_strength: int = Field(..., gt=0, le=100)


class DrinkCreate(DrinkBase):
    pass


class DrinkDB(DrinkBase):
    id: int

    class Config:
        orm_mode = True


class DrinkUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    average_strength: Optional[int] = Field(None, gt=0, le=100)
