"""Настройки для работы с объектами User."""
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import PASSWORD_GE_THREE, PASSWORD_NE_EMAIL, TOKEN_URL
from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

bearer_transport = BearerTransport(tokenUrl=TOKEN_URL)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
            self, password: str, user: Union[UserCreate, User]) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason=PASSWORD_GE_THREE)
        if user.email in password:
            raise InvalidPasswordException(
                reason=PASSWORD_NE_EMAIL)

    async def on_after_register(
            self, user: User, request: Optional[Request] = None):
        print(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend])

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
