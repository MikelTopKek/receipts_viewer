from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.dependencies import get_receipt_interactor
from app.core.security import get_current_user_id
from app.interactors.receipt import ReceiptInteractor
from app.schemas.receipt import ReceiptCreate, ReceiptResponse


router = APIRouter(tags=["receipts"])


@router.post("/", response_model=ReceiptResponse)
async def create_receipt(
    receipt_data: ReceiptCreate,
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
        raise HTTPException(status_code=400, detail=str(e))


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

