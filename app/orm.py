from sqlalchemy import select
from app.models import Base, async_engine, async_session_factory
from app.models import UsersOrm

async def db_start():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_user(telegram_id):
    async with async_session_factory() as session:
        result = await session.execute(select(UsersOrm).where(UsersOrm.telegram_id == telegram_id))
        user = result.scalars().first()

        if user is None:
            new_user = UsersOrm(telegram_id=telegram_id)
            session.add(new_user)
            await session.commit()

async def is_in_white_list(telegram_id):
    async with async_session_factory() as session:
        result = await session.execute(select(UsersOrm.telegram_id).where(UsersOrm.telegram_id == telegram_id))
        return result.scalar_one_or_none() is not None