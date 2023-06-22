from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения
    """
    app_title: str = 'Кошачий благотворительный фонд'
    app_description: str = 'Позволяет собирать пожертвования'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'Secret'

    class Config:
        env_file = '.env'


settings = Settings()
