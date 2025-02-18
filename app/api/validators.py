from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.drink import drink_crud
from app.models.drink import Drink


async def check_drink_exists_by_name(
        drink_name: str,
        session: AsyncSession
) -> Drink:
    drink = await drink_crud.get_drink_by_name(drink_name, session)
    if not drink:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Напиток с таким названием не найден'
        )
    return drink


async def check_drink_already_exists(
        drink_name: str,
        session: AsyncSession
) -> None:
    drink = await drink_crud.get_drink_by_name(drink_name, session)
    if drink:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Напиток с таким названием уже существует'
        )
