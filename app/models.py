from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

async_engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass

class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]

