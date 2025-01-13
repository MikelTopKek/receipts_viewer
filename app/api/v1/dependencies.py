from fastapi import Depends

from app.conf.settings import settings
from app.db.base import Database
from app.interactors.user import UserInteractor
from app.repositories.user import UserRepository


def get_db():
    """Return db instance"""
    return Database(settings.sqlalchemy_database_uri)


def get_user_repo(db: Database = Depends(get_db)):
    """Return user repo"""
    return UserRepository(db)


def get_user_interactor(repo: UserRepository = Depends(get_user_repo)):
    """Return user interactor"""
    return UserInteractor(repo)
