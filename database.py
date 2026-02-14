from __future__ import annotations

import datetime
from sqlalchemy import BigInteger, String, DateTime, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import DB_URL

engine = create_async_engine(DB_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    dialect: Mapped[str] = mapped_column(String(20), default="")
    script: Mapped[str] = mapped_column(String(10), default="")
    style: Mapped[str] = mapped_column(String(20), default="")
    ui_language: Mapped[str] = mapped_column(String(5), default="ru")
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_or_create_user(telegram_id: int) -> User:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            user = User(telegram_id=telegram_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user


async def update_user_dialect(telegram_id: int, dialect: str) -> User:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            user = User(telegram_id=telegram_id, dialect=dialect)
            session.add(user)
        else:
            user.dialect = dialect
        await session.commit()
        await session.refresh(user)
        return user


async def update_user_script(telegram_id: int, script: str) -> User:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            user = User(telegram_id=telegram_id, script=script)
            session.add(user)
        else:
            user.script = script
        await session.commit()
        await session.refresh(user)
        return user


async def update_user_style(telegram_id: int, style: str) -> User:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            user = User(telegram_id=telegram_id, style=style)
            session.add(user)
        else:
            user.style = style
        await session.commit()
        await session.refresh(user)
        return user


async def update_user_language(telegram_id: int, language: str) -> User:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            user = User(telegram_id=telegram_id, ui_language=language)
            session.add(user)
        else:
            user.ui_language = language
        await session.commit()
        await session.refresh(user)
        return user
