
from app.db.base import Database
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """User repository for interacting with db"""

    def __init__(self, db: Database):
        self.db = db

    async def create(self, email: str, password: str, **kwargs) -> User:
        """Creating user in db"""
        return await self.db.get_or_create(
            table=User,
            keys={"email": email},
            defaults={"password": password, **kwargs},
        )

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email"""
        return await self.db.get(User, User.email == email)

    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by user_id"""
        return await self.db.get(User, User.id == user_id)

    async def update_password(self, user_id: int, new_password: str) -> User | None:
        """Update user`s password"""
        return await self.db.update(table=User,
                                    obj_id=user_id,
                                    values={"password": new_password})

    async def update(self, user_id: int, data: dict) -> User | None:
        """Update user`s data"""
        return await self.db.update(table=User,
                                    obj_id=user_id,
                                    values=data)
