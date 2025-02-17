from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Конвертер напитков'
    database_url: str = 'sqlite+aiosqlite:///./drinks_converter.db'
    secret: str = 'secret'

    class Config:
        env_file = '.env'

settings = Settings()