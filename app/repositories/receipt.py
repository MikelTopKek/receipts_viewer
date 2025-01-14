from app.models.receipt import Receipt
from app.db.base import Database
from app.schemas.receipt import ReceiptResponse


class ReceiptRepository:
    """Repository with db requests for receipts"""

    def __init__(self, db: Database):
        self.db = db

    async def create(self, receipt_data: dict) -> Receipt:
        """Create receipt in db"""

        receipt = Receipt(**receipt_data)
        return await self.db.create(receipt)

    async def get_by_id(self, receipt_id: int) -> ReceiptResponse | None:
        """Get receipt by id"""

        return await self.db.get(Receipt, Receipt.id == receipt_id)

    async def get_user_receipts(self, user_id: int) -> list[Receipt]:
        """Return all user receipts"""

        return await self.db.get_all(
            Receipt,
            Receipt.user_id == user_id,
        )
