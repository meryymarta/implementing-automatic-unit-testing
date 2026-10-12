import pytest
from unittest.mock import Mock
from campusgo.orders import Order, Wallet, order_total


def test_ten_percent_discount_at_subtotal_50000():
    # Arrange
    price = 25000
    qty = 2
    promo = True
    
    # Act
    total = order_total(price, qty, promo)
    
    # Assert
    assert total == 45000

def test_order_total_becomes_67500():
    total = order_total(22500, 3, False)
    assert total == 67500

def test_error_message_contains_qty():
    with pytest.raises(ValueError) as err:
        order_total(25000, 0)
    assert "qty" in str(err.value)

def test_floating_point_is_close_to_0_3():
    value = 0.1 + 0.2
    assert value == pytest.approx(0.3)

def test_zero_qty_is_rejected():
    with pytest.raises(ValueError) as err:
        order_total(25000, 0)
    assert "qty" in str(err.value)

def test_negative_qty_is_rejected():
    with pytest.raises(ValueError) as err:
        order_total(25000, -5)
    assert "qty" in str(err.value)


@pytest.fixture
def processing_order():
    order = Order(id="ORD-T003", owner="U-01", total=25000)
    order.status = "PROCESSING"
    yield order
    order.delete()

def test_tc_ord_003_cancel_processing_order_is_rejected(processing_order):
    result = processing_order.cancel(by="U-01")
    assert result.rejected is True
    assert "processed" in result.message
    assert processing_order.status == "PROCESSING"
    assert processing_order.tenant_notifications == []

@pytest.mark.parametrize("price, qty, promo, expected", [
    (25000, 1, True, 25000),
    (25000, 2, True, 45000),
    (25000, 3, True, 67500),
    (25000, 2, False, 50000),
    (26000, 2, True, 46800),
])
def test_discount_br_07(price, qty, promo, expected):
    assert order_total(price, qty, promo) == expected

def test_failed_payment_leaves_balance_unchanged():
    provider = Mock()
    provider.charge.return_value = {"status": "REJECTED"}
    wallet = Wallet(balance=24000, provider=provider)

    result = wallet.pay(25000)

    assert result.success is False
    assert wallet.balance == 24000
    provider.charge.assert_called_once_with(25000)

def test_accepted_payment_with_sufficient_balance_drops_to_zero():
    provider = Mock()
    provider.charge.return_value = {"status": "ACCEPTED"}
    wallet = Wallet(balance=25000, provider=provider)

    result = wallet.pay(25000)

    assert result.success is True
    assert wallet.balance == 0
    provider.charge.assert_called_once_with(25000)


def test_accepted_payment_with_insufficient_balance_leaves_balance_unchanged():
    provider = Mock()
    provider.charge.return_value = {"status": "ACCEPTED"}
    wallet = Wallet(balance=24000, provider=provider)

    result = wallet.pay(25000)

    assert result.success is False
    assert wallet.balance == 24000