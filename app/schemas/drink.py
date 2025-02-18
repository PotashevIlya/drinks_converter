from pydantic import BaseModel, Field, PositiveInt


class DrinkBase(BaseModel):
    name: str = Field(..., max_length=50)
    average_strength: int = Field(..., gt=0, le=100)


class DrinkCreate(DrinkBase):
    pass


class DrinkUpdate(DrinkBase):
    pass


class DrinkDB(DrinkBase):
    id: int

    class Config:
        orm_mode = True
