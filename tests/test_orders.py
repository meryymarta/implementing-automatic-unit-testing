import pytest
from campusgo.orders import order_total

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