from dataclasses import dataclass

def order_total(unit_price, qty, has_promo=False):
    if qty <= 0:
        raise ValueError("qty must be greater than 0")
    subtotal = unit_price * qty
    if has_promo and subtotal >= 50000:
        return int(subtotal * 0.9)
    return subtotal


@dataclass
class Result:
    rejected: bool
    message: str


class Order:
    def __init__(self, id, owner, total):
        self.id, self.owner, self.total = id, owner, total
        self.status = "UNPAID"
        self.tenant_notifications = []

    def cancel(self, by):
        if self.status == "PROCESSING":
            return Result(rejected=True, message="Order is being processed")
        self.status = "CANCELLED"
        self.tenant_notifications.append("cancelled")
        return Result(rejected=False, message="Cancelled")
    
    def delete(self):
        self.status = "DELETED"
        self.tenant_notifications.clear()

@dataclass
class PaymentResult:
    success: bool
    message: str = ""


class Wallet:
    def __init__(self, balance, provider):
        self.balance = balance
        self.provider = provider

    def pay(self, amount):
        response = self.provider.charge(amount)
        if response["status"] == "ACCEPTED" and self.balance >= amount:
            self.balance -= amount
            return PaymentResult(success=True, message="Payment accepted")
        return PaymentResult(success=False, message="Payment rejected")