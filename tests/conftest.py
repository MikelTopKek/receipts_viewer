
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.dependencies import (get_receipt_interactor, get_user_interactor,
                                  get_user_repo)
from app.api.receipts import router as receipt_router
from app.interactors.receipt import ReceiptInteractor
from app.interactors.user import UserInteractor
from app.repositories.user import UserRepository
from app.schemas.receipt import PaymentCreate, PaymentType, ProductCreate


class MockDB:
    """Mock database class with async methods"""
    async def get(self, *args, **kwargs):  # noqa: ARG002
        """Mocked get request"""
        return

    async def get_or_create(self, *args, **kwargs):  # noqa: ARG002
        """Mocked get request"""
        return

    async def update(self, *args, **kwargs):  # noqa: ARG002
        """Mocked get request"""
        return


@pytest.fixture
def mock_user_repo():
    """Create mock for UserRepository"""
    repo = AsyncMock(spec=UserRepository)
    repo.db = mock_db
    repo.get_by_email.return_value = None
    repo.create.return_value = None
    return repo


@pytest.fixture
def mock_user_interactor(mock_user_repo):
    """Mocked UserInteractor with mocked UserRepository"""
    return UserInteractor(mock_user_repo)


@pytest.fixture
def receipt_repo():
    """Mocked receipt repo"""
    return AsyncMock()


@pytest.fixture
def interactor(receipt_repo):
    """Receipt interactor with mocked repo"""
    return ReceiptInteractor(receipt_repo)


@pytest.fixture
def valid_products():
    """Valid products"""
    return [
        ProductCreate(
            name="Test Product 1",
            price=Decimal("10.50"),
            quantity=Decimal("2"),
        ),
        ProductCreate(
            name="Test Product 2",
            price=Decimal("25.75"),
            quantity=Decimal("1"),
        ),
    ]


@pytest.fixture
def invalid_email() -> str:
    """Invalid email"""
    return "non-existent@example.com"


@pytest.fixture
def valid_email() -> str:
    """Valid email"""
    return "user@example.com"


@pytest.fixture
def hashed_password() -> str:
    """Hashed password"""
    return "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKxcQw/gMybLqYy"


@pytest.fixture
def valid_password() -> str:
    """Valid password"""
    return "valid_password"


@pytest.fixture
def invalid_password() -> str:
    """Invalid password"""
    return "invalid_password"


@pytest.fixture
def valid_public_id() -> str:
    """Valid public_id"""
    return "test_public_receipt_id"


@pytest.fixture
def invalid_public_id() -> str:
    """Valid public_id"""
    return "non-existent_test_public_receipt_id"


@pytest.fixture
def receipt_text() -> str:
    """Receipt in text format"""
    return "Some formatted receipt text"


@pytest.fixture
def valid_payment():
    """Payment"""
    return PaymentCreate(
        payment_type=PaymentType.CASH,
        amount=Decimal("50.00"),
    )


@pytest.fixture
def mock_db():
    """Mocked postgres db"""
    return MockDB()


@pytest.fixture
def mock_user():
    """Mocked user data"""
    return {
        "id": 1,
        "email": "test@example.com",
        "password": "hashed_password",
        "first_name": "Test",
        "last_name": "User",
        "is_active": True,
        "is_superuser": False,
    }


@pytest.fixture
def app(mock_user_interactor, mock_user_repo):
    """Create test application with mocked dependencies"""
    app = FastAPI()

    from app.api import auth
    app.include_router(auth.router, prefix="/api/users")
    async def get_test_receipt_interactor():
        return ReceiptInteractor(receipt_repo)
    app.dependency_overrides[get_receipt_interactor] = get_test_receipt_interactor

    # Override dependencies
    app.dependency_overrides[get_user_interactor] = lambda: mock_user_interactor
    app.dependency_overrides[get_user_repo] = lambda: mock_user_repo
    app.include_router(receipt_router, prefix="/receipts")

    return app


@pytest.fixture
def client(app):
    """Test FastAPI client"""
    return TestClient(app)
