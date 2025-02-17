import contextlib
from csv import DictReader

from app.core.db import get_async_session
from app.models import Drink


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


async def import_objects():
    with open('app/drinks_data.csv', 'r', encoding='utf-8') as file:
        async with get_async_session_context() as session:
            for record in DictReader(file):
                session.add(Drink(**record))
                await session.commit()
