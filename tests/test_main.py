# 픽스처(fixture)를 정의
# 픽스처는 테스트에서 반복적으로 사용되는 설정이나 데이터를 한 곳에 모아 관리하는 개념

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from api.db import get_db, Base
from api.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def async_client() -> AsyncClient: # 비동기식 접속을 위한 엔진과 세션을 작성
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)