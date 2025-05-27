import os
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

DB_URL = os.environ.get("DB_URL")
# DB_URL examples
# POSTGRES: postgresql+asyncpg://postgres:postgres@db:5432/foo
# MARIADB: mysql+aiomysql://user:pass@db:3306/foo
engine = create_async_engine(DB_URL, echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
