from __future__ import annotations

import datetime
from datetime import timedelta

from sqlalchemy import BigInteger, Boolean, String, DateTime, func, select
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
    ref_source: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    is_pro: Mapped[bool] = mapped_column(Boolean, default=False)
    pro_expires_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True, default=None)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )


class VoiceLog(Base):
    __tablename__ = "voice_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, index=True)
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


async def reset_user_settings(telegram_id: int, ref_source: str | None = None) -> User:
    """Reset user settings for re-onboarding. Save ref_source only on first creation."""
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            user = User(telegram_id=telegram_id, ref_source=ref_source)
            session.add(user)
        else:
            user.dialect = ""
            user.script = ""
            user.style = ""
            # Don't overwrite ref_source on re-/start
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


# --- Voice logging ---


async def log_voice_message(telegram_id: int) -> None:
    """Log a voice message interaction."""
    async with async_session() as session:
        session.add(VoiceLog(telegram_id=telegram_id))
        await session.commit()


# --- Promo codes ---


async def activate_promo(telegram_id: int, days: int) -> User:
    """Activate pro status for a user."""
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            user = User(telegram_id=telegram_id, is_pro=True,
                        pro_expires_at=datetime.datetime.utcnow() + timedelta(days=days))
            session.add(user)
        else:
            user.is_pro = True
            user.pro_expires_at = datetime.datetime.utcnow() + timedelta(days=days)
        await session.commit()
        await session.refresh(user)
        return user


# --- Admin stats ---


async def get_admin_stats() -> dict:
    """Get statistics for admin dashboard."""
    now = datetime.datetime.utcnow()
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    async with async_session() as session:
        # Total users
        total = (await session.execute(select(func.count(User.id)))).scalar() or 0

        # New in 24h
        new_24h = (await session.execute(
            select(func.count(User.id)).where(User.created_at >= day_ago)
        )).scalar() or 0

        # New in 7 days
        new_7d = (await session.execute(
            select(func.count(User.id)).where(User.created_at >= week_ago)
        )).scalar() or 0

        # Top ref sources
        ref_rows = (await session.execute(
            select(User.ref_source, func.count(User.id))
            .group_by(User.ref_source)
            .order_by(func.count(User.id).desc())
            .limit(10)
        )).all()

        ref_stats = []
        for source, count in ref_rows:
            ref_stats.append((source or "(прямой)", count))

        # Voice messages today
        voices_today = (await session.execute(
            select(func.count(VoiceLog.id)).where(VoiceLog.created_at >= today_start)
        )).scalar() or 0

        # Pro users
        pro_count = (await session.execute(
            select(func.count(User.id)).where(User.is_pro == True)  # noqa: E712
        )).scalar() or 0

    return {
        "total": total,
        "new_24h": new_24h,
        "new_7d": new_7d,
        "ref_stats": ref_stats,
        "voices_today": voices_today,
        "pro_count": pro_count,
    }
