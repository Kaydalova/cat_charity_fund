from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject

from app.crud.base import CRUDBase

class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession) -> Optional[int]:
        """
        Функция возвращает id проекта, если проект с указанным именем существует.
        Если проект еще не создан - вернет None.
        """
        project_name_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name))
        return project_name_id.scalars().first()

charity_project_crud = CRUDCharityProject(CharityProject)