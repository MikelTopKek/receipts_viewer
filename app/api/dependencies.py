from fastapi import Depends

from app.conf.settings import settings
from app.db.base import Database
from app.interactors.receipt import ReceiptInteractor
from app.interactors.user import UserInteractor
from app.repositories.receipt import ReceiptRepository
from app.repositories.user import UserRepository


def get_db() -> Database:
    """Return db instance"""
    return Database(settings.sqlalchemy_database_uri)


def get_user_repo(db: Database = Depends(get_db)) -> UserRepository:
    """Return user repo"""
    return UserRepository(db)


def get_user_interactor(repo: UserRepository = Depends(get_user_repo)) -> UserInteractor:
    """Return user interactor"""
    return UserInteractor(repo)


def get_receipt_repo(db: Database = Depends(get_db)) -> ReceiptRepository:
    """Return receipt repo"""
    return ReceiptRepository(db)


def get_receipt_interactor(repo: ReceiptRepository = Depends(get_receipt_repo)) -> ReceiptInteractor:
    """Return receipt interactor"""
    return ReceiptInteractor(repo)
