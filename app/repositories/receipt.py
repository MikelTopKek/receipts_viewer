from sqlalchemy import func, select

from app.models.receipt import Receipt
from app.db.base import Database
from app.schemas.receipt import ReceiptFilter, ReceiptResponse


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

    async def get_filtered(
        self,
        user_id: int,
        filters: ReceiptFilter,
        limit: int,
        offset: int,
    ) -> tuple[list[Receipt], int]:
        """Make request to db and return filtered receipts data"""

        # async with self.db._async_session_scope("receipts", "get_filtered") as session:
        #     query = select(Receipt).where(Receipt.user_id == user_id)

        #     if filters.date_from:
        #         query = query.where(Receipt.created >= filters.date_from)

        #     if filters.date_to:
        #         query = query.where(Receipt.created <= filters.date_to)

        #     if filters.min_amount:
        #         query = query.where(Receipt.total_amount >= filters.min_amount)

        #     if filters.max_amount:
        #         query = query.where(Receipt.total_amount <= filters.max_amount)

        #     if filters.payment_type:
        #         query = query.where(Receipt.payment_type == filters.payment_type)

        #     count_query = select(func.count()).select_from(query.subquery())
        #     total = await session.scalar(count_query)

        #     query = query.order_by(Receipt.created.desc())
        #     query = query.offset(offset).limit(limit)

        #     result = await session.execute(query)
        #     receipts = result.scalars().all()

        #     return receipts, total

        query = (
            select(Receipt)
            .order_by(Receipt.created.desc())
            # .options(
            #     selectinload(Receipt.totals)
            # )
        )

        if user_id is not None:
            query = query.where(Receipt.user_id == user_id)
        if filters.min_amount:
            query = query.where(Receipt.total_amount >= filters.min_amount)
        if filters.max_amount:
            query = query.where(Receipt.total_amount <= filters.max_amount)
        if filters.date_from is not None:
            query = query.where(Receipt.created >= filters.date_from)
        if filters.date_to is not None:
            query = query.where(Receipt.created <= filters.date_to)
        if filters.payment_type:
            query = query.where(Receipt.payment_type == filters.payment_type)


        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute_query(Receipt, count_query))
        print(total)
        # Apply pagination
        query = query.limit(limit).offset(offset)

        result = await self.db.execute_query(Receipt, query)

        return list(result), total
