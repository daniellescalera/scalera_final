# Standard library imports
from builtins import Exception, range, str
from datetime import timedelta
from uuid import uuid4
from unittest.mock import AsyncMock, Mock

# Third-party imports
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session
from faker import Faker
from sqlalchemy import select

# Application-specific imports
from app.main import app
from app.database import Base, Database
from app.models.user_model import User, UserRole
from app.dependencies import get_db, get_settings
from app.utils.security import hash_password
from app.utils.template_manager import TemplateManager
from app.services.email_service import EmailService
from app.services.jwt_service import create_access_token
from sqlalchemy.orm import Session

# Setup
fake = Faker()
settings = get_settings()
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(TEST_DATABASE_URL, echo=settings.debug)
AsyncTestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
AsyncSessionScoped = scoped_session(AsyncTestingSessionLocal)

# Fixtures
@pytest.fixture
def email_service():
    if settings.send_real_mail == 'true':
        return EmailService()
    else:
        mock_service = Mock(spec=EmailService)
        mock_service.send_verification_email = AsyncMock(return_value=None)
        mock_service.send_user_email = AsyncMock(return_value=None)
        return mock_service

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    try:
        Database.initialize(settings.database_url)
    except Exception as e:
        pytest.fail(f"Failed to initialize the database: {str(e)}")

@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture(scope="function")
async def db_session(setup_database):
    async with AsyncSessionScoped() as session:
        try:
            yield session
        finally:
            await session.close()

@pytest.fixture(scope="function")
async def async_client(db_session):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        app.dependency_overrides[get_db] = lambda: db_session
        try:
            yield client
        finally:
            app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def user(db_session):
    user = User(
        nickname=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        hashed_password=hash_password("MySuperPassword$1234"),
        role=UserRole.AUTHENTICATED,
        email_verified=False,
        is_locked=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def verified_user(db_session):
    user = User(
        nickname=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        hashed_password=hash_password("MySuperPassword$1234"),
        role=UserRole.AUTHENTICATED,
        email_verified=True,
        is_locked=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def unverified_user(db_session):
    user = User(
        nickname=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        hashed_password=hash_password("MySuperPassword$1234"),
        role=UserRole.AUTHENTICATED,
        email_verified=False,
        is_locked=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def locked_user(db_session):
    user = User(
        nickname=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        hashed_password=hash_password("MySuperPassword$1234"),
        role=UserRole.AUTHENTICATED,
        email_verified=True,
        is_locked=True,
        failed_login_attempts=settings.max_login_attempts,
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
async def users_with_same_role_50_users(db_session):
    fake.unique.clear()  # <--- ADD THIS to avoid IntegrityError
    users = []
    for _ in range(50):
        user = User(
            nickname=fake.unique.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            hashed_password=hash_password("MySuperPassword$1234"),
            role=UserRole.AUTHENTICATED,
            email_verified=True,
            is_locked=False,
        )
        db_session.add(user)
        users.append(user)
    await db_session.commit()
    return users

@pytest.fixture
async def admin_user(db_session):
    user = User(
        nickname="admin_user",
        email=fake.unique.email(),
        first_name="Admin",
        last_name="User",
        hashed_password=hash_password("securepassword"),
        role=UserRole.ADMIN,
        is_locked=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture
async def manager_user(db_session):
    user = User(
        nickname="manager_user",
        email=fake.unique.email(),
        first_name="Manager",
        last_name="User",
        hashed_password=hash_password("securepassword"),
        role=UserRole.MANAGER,
        is_locked=False,
    )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.fixture(scope="function")
def admin_token(admin_user):
    token_data = {"sub": str(admin_user.id), "role": admin_user.role.name}
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=30))

@pytest.fixture(scope="function")
def manager_token(manager_user):
    token_data = {"sub": str(manager_user.id), "role": manager_user.role.name}
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=30))

@pytest.fixture(scope="function")
def user_token(user):
    token_data = {"sub": str(user.id), "role": user.role.name}
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=30))
