from uuid import UUID
from typing import Optional
from datetime import date


from core.shared.value_objects import Amount
from .account import Account


class CreditCard(Account):
    def __init__(
        self,
        alias: str,
        limit: Amount,
        is_enabled: bool = True,
        main_credit_card_id: Optional[UUID] = None,
        next_closing_date: Optional[date] = None,
        next_expiring_date: Optional[date] = None,
        financing_limit: Amount = Amount(0),
        id: Optional[UUID] = None,
    ):
        super().__init__(alias, limit, is_enabled, id)
        self._main_credit_card_id = main_credit_card_id
        self._next_closing_date = next_closing_date
        self._next_expiring_date = next_expiring_date
        self._financing_limit = financing_limit
        # TODO: Expenses
        # TODO: Periods

    @property
    def main_credit_card_id(self) -> Optional[UUID]:
        'Get the ID of the main credit card.'
        return self._main_credit_card_id

    @main_credit_card_id.setter
    def main_credit_card_id(self, value: Optional[UUID]):
        'Set the ID of the main credit card.'
        if value is not None and not isinstance(value, UUID):
            raise ValueError('main_credit_card_id must be a UUID or None')
        self._main_credit_card_id = value

    @property
    def next_closing_date(self) -> Optional[date]:
        'Get the next closing date of the credit card.'
        return self._next_closing_date

    @next_closing_date.setter
    def next_closing_date(self, value: Optional[date]):
        'Set the next closing date of the credit card.'
        if value is not None and not isinstance(value, date):
            raise ValueError('next_closing_date must be a date or None')
        self._next_closing_date = value

    @property
    def next_expiring_date(self) -> Optional[date]:
        'Get the next expiring date of the credit card.'
        return self._next_expiring_date

    @next_expiring_date.setter
    def next_expiring_date(self, value: Optional[date]):
        'Set the next expiring date of the credit card.'
        if value is not None and not isinstance(value, date):
            raise ValueError('next_expiring_date must be a date or None')
        self._next_expiring_date = value

    @property
    def financing_limit(self) -> Amount:
        'Get the financing limit of the credit card.'
        return self._financing_limit

    @financing_limit.setter
    def financing_limit(self, value: Amount):
        'Set the financing limit of the credit card.'
        if value.value < 0:
            raise ValueError('financing_limit cannot be negative')
        self._financing_limit = value
