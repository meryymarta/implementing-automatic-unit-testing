def order_total(unit_price, qty, has_promo=False):
    if qty <= 0:
        raise ValueError("qty must be greater than 0")
    subtotal = unit_price * qty
    if has_promo and subtotal >= 50000:
        return int(subtotal * 0.9)
    return subtotal