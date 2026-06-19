"""
Pricing strategy abstract base class.

✅ This ABC is COMPLETE. Subclasses go in sibling files.
"""

from abc import ABC, abstractmethod
from billing_engine.money import Money


class PricingStrategy(ABC):
    """Computes the base charge for a billing period given a usage quantity.

    Subclasses MUST implement `calculate`. The method takes a non-negative
    integer `quantity` (e.g., API calls, seats, GB transferred) and returns
    a `Money` value in the strategy's configured currency.

    For strategies that ignore usage (e.g., FlatRate), `quantity` is still
    accepted but may be unused.
    """

    @abstractmethod
    def calculate(self, quantity: int) -> Money:
        """Return the charge for the given usage quantity."""
        raise NotImplementedError
class UsageBased(PricingStrategy):
    """Charges `unit_price * quantity`."""

    def __init__(self, unit_price: Money) -> None:
        if not isinstance(unit_price, Money):
            raise TypeError("unit_price must be a Money instance")

        if unit_price.amount < 0:
            raise ValueError("unit_price cannot be negative")

        self.unit_price = unit_price

    def calculate(self, quantity: int) -> Money:
        if quantity < 0:
            raise ValueError("quantity cannot be negative")

        return Money(
            self.unit_price.amount * quantity,
            self.unit_price.currency
        )