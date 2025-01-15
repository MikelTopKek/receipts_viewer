from fastapi.testclient import TestClient
import pytest
from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException, status

from app.models.receipt import Receipt
from app.schemas.receipt import PaymentCreate, PaymentType, ReceiptCreateDTO, ReceiptFilter
from app.interactors.receipt import ReceiptInteractor


@pytest.mark.asyncio
async def test_create_receipt_success(interactor: ReceiptInteractor,
                                      receipt_repo, valid_products,
                                      valid_payment: PaymentCreate,
                                      valid_public_id: str,
                                      ):
    """Test creating receipts successfully"""
    expected_products = [{
            "name": "Test Product 1",
            "price": Decimal("10.50"),
            "quantity": Decimal("2"),
            "total": Decimal("21.00"),
        }, {
            "name": "Test Product 2",
            "price": Decimal("25.75"),
            "quantity": Decimal("1"),
            "total": Decimal("25.75"),
        }]
    expected_total = Decimal("46.75") # 10.50 * 2 + 25.75 * 1
    expected_rest = Decimal("3.25") # 50.00 - 46.75
    payment_amount = Decimal("50.00")
    user_id = 1
    create_dto = ReceiptCreateDTO(
        products=valid_products,
        payment=valid_payment,
    )

    mock_receipt = MagicMock(
        id=1,
        public_id=valid_public_id,
        user_id=user_id,
        total_amount=expected_total,
        payment_type=PaymentType.CASH,
        payment_amount=payment_amount,
        rest_amount=expected_rest,
        products=expected_products,
        created=datetime.now(),
    )

    receipt_repo.create.return_value = mock_receipt

    result = await interactor.create_receipt(user_id, create_dto)

    assert result.id == mock_receipt.id
    assert result.public_id == mock_receipt.public_id
    assert result.total_amount == expected_total
    assert result.rest_amount == expected_rest
    assert len(result.products) == len(expected_products)

    receipt_repo.create.assert_called_once()
    create_args = receipt_repo.create.call_args[0][0]
    assert create_args["user_id"] == user_id
    assert create_args["total_amount"] == expected_total
    assert create_args["payment_type"] == PaymentType.CASH
    assert create_args["rest_amount"] == expected_rest


@pytest.mark.asyncio
async def test_get_receipt_success(interactor: ReceiptInteractor,
                                   receipt_repo: AsyncMock,
                                   valid_public_id: str,
                                ):
    """Test getting receipts successfully"""
    receipt_id = 1
    user_id = 1
    mock_receipt = MagicMock(
        id=receipt_id,
        user_id=user_id,
        public_id=valid_public_id,
        products=[],
        payment_type=PaymentType.CASH,
        payment_amount=Decimal("50.00"),
        total_amount=Decimal("46.75"),
        rest_amount=Decimal("3.25"),
        created=datetime.now(),
    )
    receipt_repo.get_by_id.return_value = mock_receipt

    result = await interactor.get_receipt(receipt_id, user_id)

    assert result.id == receipt_id
    assert result.public_id == mock_receipt.public_id
    receipt_repo.get_by_id.assert_called_once_with(receipt_id=receipt_id)


@pytest.mark.asyncio
async def test_get_receipt_not_found(interactor: ReceiptInteractor,
                                     receipt_repo: AsyncMock,
                                    ):
    """Test creating receipts unsuccessfully (Not found receipt)"""
    receipt_id = 999
    user_id = 1
    receipt_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await interactor.get_receipt(receipt_id, user_id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Receipt not found"


@pytest.mark.asyncio
async def test_get_receipt_wrong_user(interactor: ReceiptInteractor,
                                      receipt_repo: AsyncMock,
                                    ):
    """Test creating receipts unsuccessfully (Wrong user)"""
    receipt_id = 1
    user_id = 1
    wrong_user_id = 2
    mock_receipt = MagicMock(
        id=receipt_id,
        user_id=wrong_user_id,  # Different user
    )
    receipt_repo.get_by_id.return_value = mock_receipt

    with pytest.raises(HTTPException) as exc_info:
        await interactor.get_receipt(receipt_id, user_id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Receipt not found"


@pytest.mark.asyncio
async def test_get_filtered_receipts(interactor: ReceiptInteractor,
                                     receipt_repo: AsyncMock,
                                     valid_public_id: str,
                                    ):
    """Test getting filtered receipts successfully"""

    user_id = 1
    filters = ReceiptFilter()
    limit = 10
    offset = 0

    mock_receipts = [
        MagicMock(
            id=1,
            public_id=valid_public_id,
            products=[],
            payment_type=PaymentType.CASH,
            payment_amount=Decimal("50.00"),
            total_amount=Decimal("46.75"),
            rest_amount=Decimal("3.25"),
            created=datetime.now(),
        ),
        MagicMock(
            id=2,
            public_id=f"{valid_public_id}_2",
            products=[],
            payment_type=PaymentType.CASHLESS,
            payment_amount=Decimal("30.00"),
            total_amount=Decimal("30.00"),
            rest_amount=Decimal("0.00"),
            created=datetime.now(),
        ),
    ]
    total_count = 2

    receipt_repo.get_filtered.return_value = (mock_receipts, total_count)

    results, total = await interactor.get_filtered_receipts(
        user_id=user_id,
        filters=filters,
        limit=limit,
        offset=offset,
    )

    assert len(results) == len(mock_receipts)
    assert total == total_count
    receipt_repo.get_filtered.assert_called_once_with(
        user_id=user_id,
        filters=filters,
        limit=limit,
        offset=offset,
    )


@pytest.mark.asyncio
async def test_get_receipt_text_success(interactor: ReceiptInteractor,
                                        receipt_repo: AsyncMock,
                                        valid_public_id: str,
                                    ):
    """Test gettinig receipt`s text format successfully"""
    line_width = 32
    mock_receipt = Receipt(
        id=1,
        public_id=valid_public_id,
        user_id=1,
        products=[{
            "name": "Test Product",
            "price": Decimal("10.50"),
            "quantity": Decimal("2"),
            "total": Decimal("21.00"),
        }],
        payment_type=PaymentType.CASH,
        payment_amount=Decimal("25.00"),
        total_amount=Decimal("21.00"),
        rest_amount=Decimal("4.00"),
        created=datetime.now(),
    )
    receipt_repo.get_by_public_id.return_value = mock_receipt

    result = await interactor.get_receipt_text(valid_public_id, line_width)

    assert "ФОП Джонсонюк Борис" in result
    assert "Test Product" in result
    assert "21.00" in result
    assert "Дякуємо за покупку!" in result
    receipt_repo.get_by_public_id.assert_called_once_with(valid_public_id)


@pytest.mark.asyncio
async def test_get_receipt_text_not_found(interactor: ReceiptInteractor,
                                          receipt_repo: AsyncMock,
                                          invalid_public_id: str,
                                        ):
    """Test creating receipts unsuccessfully (Not found receipt)"""

    line_width = 32
    receipt_repo.get_by_public_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await interactor.get_receipt_text(invalid_public_id, line_width)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Receipt not found"


@pytest.mark.asyncio
async def test_public_receipt_text_endpoint_success(client: TestClient,
                                                    receipt_repo: AsyncMock,
                                                    monkeypatch,
                                                    receipt_text: str,
                                                    valid_public_id: str,
                                                ):
    """Test getting receipt`s text format successfully"""
    mock_receipt = Receipt(
        id=1,
        public_id=valid_public_id,
        user_id=1,
        products=[{
            "name": "Public Test Product",
            "price": Decimal("15.50"),
            "quantity": Decimal("2"),
            "total": Decimal("31.00"),
        }],
        payment_type=PaymentType.CASH,
        payment_amount=Decimal("40.00"),
        total_amount=Decimal("31.00"),
        rest_amount=Decimal("9.00"),
        created=datetime.now(),
    )
    receipt_repo.get_by_public_id.return_value = mock_receipt

    async def mock_get_receipt_text(*args, **kwargs):
        return receipt_text

    monkeypatch.setattr(ReceiptInteractor, "get_receipt_text", mock_get_receipt_text)

    response = client.get(f"/receipts/public/{valid_public_id}?line_width=32")

    assert response.status_code == status.HTTP_200_OK
    assert response.text == receipt_text

    assert response.headers["content-type"] == "text/plain; charset=utf-8"


@pytest.mark.asyncio
async def test_public_receipt_text_endpoint_not_found(client: TestClient,
                                                      receipt_repo: AsyncMock,
                                                      invalid_public_id: str,
                                                      monkeypatch,
                                                    ):
    """Test getting receipt`s text format unsuccessfully (Not found by public_id)"""
    receipt_repo.get_by_public_id.return_value = None

    async def mock_get_receipt_text(*args, **kwargs):
        raise HTTPException(status_code=404, detail="Receipt not found")

    monkeypatch.setattr(ReceiptInteractor, "get_receipt_text", mock_get_receipt_text)

    response = client.get(f"/receipts/public/{invalid_public_id}?line_width=32")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Receipt not found"


@pytest.mark.asyncio
async def test_public_receipt_text_endpoint_invalid_width(client: TestClient,
                                                          valid_public_id: str,
                                                        ):
    """Test getting receipt`s text format unsuccessfully (Invalid width)"""

    response_min = client.get(f"/receipts/public/{valid_public_id}?line_width=19")

    response_max = client.get(f"/receipts/public/{valid_public_id}?line_width=101")

    assert response_min.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_max.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
