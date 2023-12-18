import os
import asyncio
import pytest_asyncio

from httpx import AsyncClient

from fastapi.testclient import TestClient

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from models import BaseSQLAlchemyClass
from db_conf import get_session
from main import app



DATABASE_URL_TEST = f'sqlite+aiosqlite:///./test.db'
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata = BaseSQLAlchemyClass.metadata
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_session] = override_get_async_session


@pytest_asyncio.fixture(autouse=True, scope='function')
async def prepare_database(request):
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)
    os.remove("./test.db")


# SETUP
@pytest_asyncio.fixture(scope='session', autouse=True)
def event_loop(request):
    """Экземпляр цикла событий по умолчанию для каждого тестового примера."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app=app, base_url='http://test/')


@pytest_asyncio.fixture(scope="session", autouse=True)
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app) as ac:
        yield ac