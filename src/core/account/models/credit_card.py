from uuid import UUID
from typing import Optional, List
from datetime import date


from ...expense.models.expense import Expense
from ...period.models.period import Period
from ...user import User
from .account import Account
from core.shared.value_objects import Amount


class CreditCard(Account):
    def __init__(
        self,
        owner: User,
        alias: str,
        limit: Amount,
        is_enabled: bool = True,
        main_credit_card_id: Optional[UUID] = None,
        next_closing_date: Optional[date] = None,
        next_expiring_date: Optional[date] = None,
        financing_limit: Amount = Amount(0),
        expenses: List[Expense] = [],
        periods: List[Period] = [],
        id: Optional[UUID] = None,
    ):
        super().__init__(owner, alias, limit, is_enabled, id)
        self._main_credit_card_id = main_credit_card_id
        self._next_closing_date = next_closing_date
        self._next_expiring_date = next_expiring_date
        self._financing_limit = financing_limit
        self._expenses = expenses
        self._periods = periods if periods is not None else []

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

    @property
    def available_limit(self) -> Amount:
        'Calculate the available limit of the credit card.'
        total_expenses = sum(expense.pending_amount.value for expense in self._expenses)
        return Amount(self._limit.value - total_expenses)

    @property
    def available_financing_limit(self) -> Amount:
        'Calculate the available financing limit of the credit card.'
        total_financing = sum(expense.pending_financing_amount.value for expense in self._expenses)
        return Amount(self._financing_limit.value - total_financing)

    @property
    def periods(self) -> List[Period]:
        'Get the list of periods associated with the credit card.'
        return self._periods

    @periods.setter
    def periods(self, value: List[Period]):
        'Set the list of periods associated with the credit card.'
        if not isinstance(value, list) or not all(isinstance(p, Period) for p in value):
            raise ValueError('periods must be a list of Period instances')
        self._periods = value

    @classmethod
    def from_dict(cls, data: dict) -> 'CreditCard':
        '''Create a CreditCard instance from a dictionary representation.'''
        return cls(
            owner=User.from_dict(data['owner']),
            alias=data['alias'],
            limit=Amount(data['limit']),
            is_enabled=data.get('is_enabled', True),
            main_credit_card_id=data.get('main_credit_card_id'),
            next_closing_date=data.get('next_closing_date'),
            next_expiring_date=data.get('next_expiring_date'),
            financing_limit=Amount(data.get('financing_limit', 0)),
            id=data.get('id')
        )
