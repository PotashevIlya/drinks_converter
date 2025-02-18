from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.drink import drink_crud
from app.schemas.drink import DrinkCreate, DrinkUpdate, DrinkDB
from app.api.validators import check_drink_exists


router = APIRouter()


@router.get(
    '/',
    response_model=list[DrinkDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_drinks(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров"""
    return await drink_crud.get_multi(session)


@router.get(
    '/{drink_name}',
    response_model=DrinkDB,
    dependencies=[Depends(current_superuser)]
)
async def get_drink(
    drink_name: str,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров"""
    return await check_drink_exists(drink_name, session)


@router.post(
    '/',
    response_model=DrinkDB,
    dependencies=[Depends(current_superuser)],
)
async def add_new_drink(
    drink: DrinkCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    new_drink = await drink_crud.create(drink, session)
    return new_drink


@router.patch(
    '/{drink_name}',
    response_model=DrinkDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_drink(
    drink_name: str,
    obj_in: DrinkUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров"""
    drink = await check_drink_exists(drink_name, session)
    return await drink_crud.update(drink, obj_in, session)


@router.delete(
    '/{drink_name}',
    response_model=DrinkDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_drink(
    drink_name: str,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    drink = await check_drink_exists(drink_name, session)
    return await drink_crud.remove(drink, session)
