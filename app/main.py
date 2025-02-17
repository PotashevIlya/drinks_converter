from fastapi import FastAPI
from app.core.config import settings

from app.core.init_db import import_objects

app = FastAPI(title=settings.app_title)


@app.on_event('startup')
async def startup():
    await import_objects()
