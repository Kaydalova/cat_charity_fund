from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд'
    app_description: str = 'Позволяет собирать пожертвования'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    # secret: str = 'Secret'
    # first_superuser_email: Optional[EmailStr] = None
    # first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'

settings = Settings()