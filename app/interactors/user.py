from fastapi import status
from psycopg2 import IntegrityError
import sqlalchemy

from app.core.exceptions import AppErrorException
from app.core.security import get_password_hash, verify_password
from app.repositories.user import UserRepository
from app.schemas.user import UserCreateDTO, UserUpdateDTO


class UserInteractor:
    """Interactor for users` business logic"""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_data: UserCreateDTO) -> dict:
        """
        Check if user exists, hash password and create user

        Args:
            user_data (UserCreateDTO): data for creating user

        Returns:
            dict: created user`s info
        """
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise AppErrorException(
                message="User with this email already exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        hashed_password = get_password_hash(user_data.password)
        user = await self.user_repo.create(
            email=user_data.email,
            password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

    async def authenticate(self, email: str, password: str) -> dict | None:
        """
        Authenticate user by email

        Args:
            email (str): user`s email
            password (str): user`s password

        Returns:
            dict | None: user`s data
        """
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password):
            return None

        return {
            "id": user.id,
            "email": user.email,
        }


    async def update_user(self, user_id: int, user_data: UserUpdateDTO) -> dict:
        """
        Update user in db by id using user_data

        Args:
            user_id (int): user`s id
            user_data (UserUpdateDTO): contain fields which need to update

        Returns:
            dict: updated user`s data
        """
        try:
            user = await self.user_repo.update(user_id, user_data.model_dump(exclude_unset=True))
        except sqlalchemy.exc.IntegrityError:
            raise ValueError("Email already used")
            
        if not user:
            raise ValueError("User not found")
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

    async def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
    ) -> bool:
        """
        Update user`s password

        Args:
            user_id (int): user`s id
            old_password (str): old user`s password
            new_password (str): new user`s id

        Returns:
            bool: if got any errors returns False, else returns True
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user or not verify_password(old_password, user.password):
            return False

        await self.user_repo.update_password(user_id, get_password_hash(new_password))
        return True
