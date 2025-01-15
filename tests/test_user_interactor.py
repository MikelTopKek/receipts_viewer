from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status

from app.core.exceptions import AppErrorException
from app.interactors.user import UserInteractor
from app.schemas.user import UserCreateDTO, UserUpdateDTO


@pytest.mark.asyncio
async def test_create_user_success(mock_user_interactor: UserInteractor,
                                   mock_user_repo: AsyncMock,
                                   valid_email: str,
                                   valid_password: str,
                                   hashed_password: str,
                                ):
    """Test successful user creation"""
    user_data = UserCreateDTO(
        email=valid_email,
        password=valid_password,
        first_name="Test",
        last_name="User",
    )

    mock_user_repo.get_by_email.return_value = None
    mock_user_repo.create.return_value = AsyncMock(
        id=1,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )

    with patch("app.core.security.get_password_hash", return_value=hashed_password):
        result = await mock_user_interactor.create_user(user_data)

    assert result["email"] == user_data.email
    assert result["first_name"] == user_data.first_name
    mock_user_repo.get_by_email.assert_called_once_with(user_data.email)
    mock_user_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_existing_email(mock_user_interactor: UserInteractor,
                                          mock_user_repo: AsyncMock,
                                          valid_email: str,
                                          valid_password: str,
                                        ):
    """Test user creation with existing email"""
    user_data = UserCreateDTO(
        email=valid_email,
        password=valid_password,
    )

    mock_user_repo.get_by_email.return_value = AsyncMock(
        email=user_data.email,
    )

    with pytest.raises(AppErrorException) as exc_info:
        await mock_user_interactor.create_user(user_data)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "User with this email already exists" in str(exc_info.value)
    mock_user_repo.create.assert_not_called()


@pytest.mark.asyncio
async def test_authenticate_success(mock_user_interactor: UserInteractor,
                                    mock_user_repo: AsyncMock,
                                    valid_email: str,
                                    valid_password: str,
                                    hashed_password: str,
                                ):
    """Test successful user authentication"""

    user_id = 1

    mock_user = AsyncMock()
    mock_user.id = user_id
    mock_user.email = valid_email
    mock_user.password = hashed_password

    mock_user_repo.get_by_email.return_value = mock_user

    with patch("app.interactors.user.verify_password", return_value=True):
        result = await mock_user_interactor.authenticate(valid_email, valid_password)

    assert result is not None
    assert result["id"] == user_id
    assert result["email"] == valid_email
    mock_user_repo.get_by_email.assert_called_once_with(valid_email)


@pytest.mark.asyncio
async def test_authenticate_invalid_credentials(mock_user_interactor: UserInteractor,
                                                mock_user_repo: AsyncMock,
                                                valid_email: str,
                                                invalid_password: str,
                                                hashed_password: str,
                                            ):
    """Test authentication with invalid credentials"""

    mock_user = AsyncMock()
    mock_user.id = 1
    mock_user.email = valid_email
    mock_user.password = hashed_password

    mock_user_repo.get_by_email.return_value = mock_user

    with patch("app.core.security.pwd_context") as mock_pwd_context:
        mock_pwd_context.verify.return_value = False

        result = await mock_user_interactor.authenticate(valid_email, invalid_password)

    assert result is None

    mock_user_repo.get_by_email.assert_called_once_with(valid_email)
    mock_pwd_context.verify.assert_called_once_with(invalid_password, hashed_password)


@pytest.mark.asyncio
async def test_update_user_success(mock_user_interactor: UserInteractor,
                                   mock_user_repo: AsyncMock,
                                   valid_email: str,
                                ):
    """Test successful user update"""
    user_id = 1
    update_data = UserUpdateDTO(
        first_name="Updated",
        last_name="Name",
    )

    mock_user_repo.update.return_value = AsyncMock(
        id=user_id,
        email=valid_email,
        first_name=update_data.first_name,
        last_name=update_data.last_name,
    )

    result = await mock_user_interactor.update_user(user_id, update_data)

    assert result["first_name"] == update_data.first_name
    assert result["last_name"] == update_data.last_name
    mock_user_repo.update.assert_called_once_with(
        user_id,
        update_data.model_dump(exclude_unset=True),
    )


@pytest.mark.asyncio
async def test_authenticate_user_not_found(mock_user_interactor: UserInteractor,
                                           mock_user_repo: AsyncMock,
                                           invalid_email: str,
                                           valid_password: str,
                                        ):
    """Test failed authentication when user not found"""

    mock_user_repo.get_by_email.return_value = None

    result = await mock_user_interactor.authenticate(invalid_email, valid_password)

    assert result is None
    mock_user_repo.get_by_email.assert_called_once_with(invalid_email)


@pytest.mark.asyncio
async def test_authenticate_wrong_password(mock_user_interactor: UserInteractor,
                                           mock_user_repo: AsyncMock,
                                           invalid_email: str,
                                           valid_password: str,
                                           hashed_password: str,
                                        ):
    """Test failed authentication with wrong password"""
    mock_user = AsyncMock()
    mock_user.password = hashed_password
    mock_user_repo.get_by_email.return_value = mock_user

    with patch("app.interactors.user.verify_password", return_value=False):
        result = await mock_user_interactor.authenticate(invalid_email, valid_password)

    assert result is None, f"Failed authentication with wrong password {valid_password}"

    mock_user_repo.get_by_email.assert_called_once_with(invalid_email)

@pytest.mark.asyncio
async def test_change_password_success(mock_user_interactor: UserInteractor,
                                       mock_user_repo: AsyncMock,
                                    ):
    """Test successful password change with proper mocking"""
    user_id = 1
    old_password = "old_password"
    new_password = "new_password"

    hashed_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKxcQw/gMybLqYy"

    mock_user = AsyncMock()
    mock_user.id = user_id
    mock_user.password = hashed_password

    mock_user_repo.get_by_id.return_value = mock_user
    mock_user_repo.update_password.return_value = mock_user

    with patch("app.core.security.pwd_context") as mock_pwd_context:
        mock_pwd_context.verify.return_value = True
        mock_pwd_context.hash.return_value = "new_hashed_password"

        result = await mock_user_interactor.change_password(user_id, old_password, new_password)

    assert result is True, "Successful password changing"

    mock_user_repo.get_by_id.assert_called_once_with(user_id)
    mock_pwd_context.verify.assert_called_once_with(old_password, hashed_password)
    mock_user_repo.update_password.assert_called_once_with(user_id, "new_hashed_password")


@pytest.mark.asyncio
async def test_change_password_invalid_old_password(mock_user_interactor: UserInteractor,
                                                    mock_user_repo: AsyncMock,
                                                ):
    """Test password change with invalid old password"""
    user_id = 1
    old_password = "wrong_password"
    new_password = "new_password"

    hashed_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKxcQw/gMybLqYy"

    mock_user = AsyncMock()
    mock_user.id = user_id
    mock_user.password = hashed_password

    mock_user_repo.get_by_id.return_value = mock_user

    with patch("app.core.security.pwd_context") as mock_pwd_context:
        mock_pwd_context.verify.return_value = False

        result = await mock_user_interactor.change_password(user_id, old_password, new_password)

    assert result is False, "Unsuccessful password changing"

    mock_user_repo.get_by_id.assert_called_once_with(user_id)
    mock_pwd_context.verify.assert_called_once_with(old_password, hashed_password)
    mock_user_repo.update_password.assert_not_called()
