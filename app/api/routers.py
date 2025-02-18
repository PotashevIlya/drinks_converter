from fastapi import APIRouter

from app.api.endpoints import drink_router, user_router


main_router = APIRouter()
main_router.include_router(
    drink_router,
    prefix='/drink',
    tags=['Drinks']
)
main_router.include_router(user_router)
