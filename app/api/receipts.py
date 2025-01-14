from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.api.dependencies import get_receipt_interactor
from app.core.security import get_current_user_id
from app.interactors.receipt import ReceiptInteractor
from app.schemas.receipt import PaymentType, ReceiptCreateDTO, ReceiptFilter, ReceiptResponse


router = APIRouter(tags=["receipts"])


@router.post("/", response_model=ReceiptResponse)
async def create_receipt(
    receipt_data: ReceiptCreateDTO,
    current_user_id: int = Depends(get_current_user_id),
    interactor: ReceiptInteractor = Depends(get_receipt_interactor),
):
    """
    Creating receipt in db for current authorized user. Need to be authorized.
    Payment type can be CASH or CASHLESS.
    """
    try:
        return await interactor.create_receipt(current_user_id, receipt_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=dict)
async def get_receipts(
    date_from: date | None = None,
    date_to: date | None = None,
    min_amount: Decimal | None = Query(default=0, ge=0),
    max_amount: Decimal | None = Query(default=0, ge=0),
    payment_type: PaymentType | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user_id: int = Depends(get_current_user_id),
    interactor: ReceiptInteractor = Depends(get_receipt_interactor),
):
    """
    Return filtered user`s receipts.
    By default all filters are NULL. It means that nullable filters are skipped for request.
    Limit from 1 to 100.
    Payment type can be 'cash' or 'cashless'.
    Date formatted as "YYYY-MM-DD HH-MM-SS"
    """
    filters = ReceiptFilter(
        date_from=date_from,
        date_to=date_to,
        min_amount=min_amount,
        max_amount=max_amount,
        payment_type=payment_type,
    )

    receipts, total = await interactor.get_filtered_receipts(
        user_id=current_user_id,
        filters=filters,
        limit=limit,
        offset=offset,
    )

    return {
        "items": receipts,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{receipt_id}", response_model=ReceiptResponse)
async def get_receipt(
    receipt_id: int,
    current_user_id: int = Depends(get_current_user_id),
    interactor: ReceiptInteractor = Depends(get_receipt_interactor),
):
    """
    Return receipt data by its id from db for current user.
    Need to be authorized.
    """
    return await interactor.get_receipt(receipt_id, current_user_id)

