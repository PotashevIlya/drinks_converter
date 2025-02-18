from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.drink import Drink


class CRUDDrink(CRUDBase):

    async def get_drink_by_name(
            self,
            drink_name: str,
            session: AsyncSession
    ) -> Optional[Drink]:
        drink = await session.execute(
            select(Drink).where(Drink.name == drink_name.capitalize())
        )
        return drink.scalars().first()


drink_crud = CRUDDrink(Drink)
