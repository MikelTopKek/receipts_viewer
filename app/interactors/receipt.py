from decimal import Decimal
from fastapi import HTTPException, status
import ujson
from app.repositories.receipt import ReceiptRepository
from app.schemas.receipt import ReceiptCreateDTO, ReceiptFilter, ReceiptResponse, ProductData


class ReceiptInteractor:
    """Interactor for business logic for receipts"""

    def __init__(self, receipt_repo: ReceiptRepository):
        self.receipt_repo = receipt_repo

    async def create_receipt(self, user_id: int, data: ReceiptCreateDTO) -> ReceiptResponse:
        """Creating receipt in db based on data from request"""

        products_with_total = []
        total_amount = Decimal("0")

        for product in data.products:
            product_total = product.price * product.quantity
            total_amount += product_total

            products_with_total.append({
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "total": product_total,
            })

        rest_amount = data.payment.amount - total_amount if data.payment.amount > total_amount else Decimal("0")

        receipt_data = {
            "user_id": user_id,
            "total_amount": total_amount,
            "payment_type": data.payment.payment_type,
            "payment_amount": data.payment.amount,
            "rest_amount": rest_amount,
            "products": ujson.loads(ujson.dumps(products_with_total)),
        }

        receipt = await self.receipt_repo.create(receipt_data)

        return ReceiptResponse(
            id=receipt.id,
            products=[ProductData(**p) for p in receipt.products],
            payment_type=data.payment.payment_type,
            payment_amount=data.payment.amount,
            total_amount=receipt.total_amount,
            rest_amount=receipt.rest_amount,
            created=receipt.created,
        )

    async def get_receipt(self, receipt_id: int, current_user_id: int) -> ReceiptResponse:
        """Get receipt data by id"""

        receipt = await self.receipt_repo.get_by_id(receipt_id=receipt_id)

        if not receipt or receipt.user_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")

        return ReceiptResponse(id=receipt_id,
                               products=receipt.products,
                               payment_type=receipt.payment_type,
                               payment_amount=receipt.payment_amount,
                               total_amount=receipt.total_amount,
                               rest_amount=receipt.rest_amount,
                               created=receipt.created,
                            )

    async def get_filtered_receipts(
        self,
        user_id: int,
        filters: ReceiptFilter,
        limit: int,
        offset: int,
    ) -> tuple[list[ReceiptResponse], int]:
        """Return receipts with fiters described in filters variable."""
        receipts, total = await self.receipt_repo.get_filtered(
            user_id=user_id,
            filters=filters,
            limit=limit,
            offset=offset,
        )

        return [
            ReceiptResponse(
                id=receipt.id,
                products=receipt.products,
                payment_type=receipt.payment_type,
                payment_amount=receipt.payment_amount,
                total_amount=receipt.total_amount,
                rest_amount=receipt.rest_amount,
                created=receipt.created,
            ) for receipt in receipts
        ], total
