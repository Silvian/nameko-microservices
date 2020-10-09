import random
from enum import Enum


class OrderStatus(Enum):
    INITIATED = "INITIATED"
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"


class Order:
    """Order object class."""

    def __init__(self, details):
        self.id = random.randint(100000, 999999)
        self.details = details
        self.status = OrderStatus.INITIATED.value

    def __str__(self):
        return f"Order id: {self.id} with details: {self.details}"
