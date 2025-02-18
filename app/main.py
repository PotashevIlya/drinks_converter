from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser, import_objects

app = FastAPI(title=settings.app_title)

app.include_router(main_router)


# @app.on_event('startup')
# async def startup():
#     await import_objects()


@app.on_event('startup')
async def startup():
    await create_first_superuser()
