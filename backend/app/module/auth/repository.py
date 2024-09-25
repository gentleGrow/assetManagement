from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.module.auth.enum import ProviderEnum
from app.module.auth.model import User


class UserRepository:
    @staticmethod
    async def get_by_social_id(session: AsyncSession, social_id: str, provider: ProviderEnum) -> User | None:
        select_instance = select(User).where(User.social_id == social_id, User.provider == provider.value)

        result = await session.execute(select_instance)
        return result.scalars().first()

    @staticmethod
    async def get(session: AsyncSession, user_id: int) -> User | None:
        select_instance = select(User).where(User.id == user_id)
        result = await session.execute(select_instance)
        return result.scalars().first()

    @staticmethod
    async def create(session: AsyncSession, new_user: User) -> User:
        session.add(new_user)
        await session.commit()
        return new_user

    @staticmethod
    async def get_by_name(session: AsyncSession, user_name: str) -> User | None:
        select_instance = select(User).where(User.nickname == user_name)
        result = await session.execute(select_instance)
        return result.scalars().first()
