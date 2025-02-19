from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.drink import drink_crud
from app.schemas.convertation import ConvertationData
from app.services.convertation_logic import convert
from app.api.validators import check_drink_exists_by_name


router = APIRouter()


@router.post(
    '/'
)
async def convertation(
        data: ConvertationData,
        session: AsyncSession = Depends(get_async_session)
):
    source_drink = await check_drink_exists_by_name(data.source_name, session)
    if data.target_name:
        target_drink = await check_drink_exists_by_name(
            data.target_name,
            session
        )
        return {
            'target_name': target_drink.name,
            'target_ml': await convert(
                source_drink,
                data.source_ml,
                target_drink
            )
        }
    results = []
    target_drinks = await drink_crud.get_multi(session)
    target_drinks.remove(source_drink)
    for target_drink in target_drinks:
        results.append(
            {'target_name': target_drink.name,
             'target_ml': await convert(
                 source_drink,
                 data.source_ml,
                 target_drink)
             }
        )
    return results
