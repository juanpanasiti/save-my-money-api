from uuid import UUID
from typing import Optional
from typing import List

from core.shared.value_objects import Month, Year, Amount
from ...shared.entity_base import EntityBase
from ...expense.models.payment import Payment


class Period(EntityBase):
    def __init__(
            self,
            month: Month,
            year: Year,
            payments: List[Payment] = [],
            id: Optional[UUID] = None,
    ):
        super().__init__(id)
        self._month = month
        self._year = year
        self._payments = payments if payments is not None else []

    @property
    def month(self) -> Month:
        'Get the month of the period.'
        return self._month

    @month.setter
    def month(self, value: Month):
        'Set the month of the period.'
        if not isinstance(value, Month):
            raise ValueError('month must be an instance of Month')
        self._month = value

    @property
    def year(self) -> Year:
        'Get the year of the period.'
        return self._year

    @year.setter
    def year(self, value: Year):
        'Set the year of the period.'
        if not isinstance(value, Year):
            raise ValueError('year must be an instance of Year')
        self._year = value

    @property
    def payments(self) -> List[Payment]:
        'Get the list of payments associated with the period.'
        return self._payments

    @payments.setter
    def payments(self, value: List[Payment]):
        'Set the list of payments associated with the period.'
        if not isinstance(value, list) or not all(isinstance(p, Payment) for p in value):
            raise ValueError('payments must be a list of Payment instances')
        self._payments = value

    @property
    def total_amount(self) -> Amount:
        'Calculate the total amount of all payments in the period.'
        total = sum(payment.amount.value for payment in self._payments)
        return Amount(total)

    @property
    def total_one_time_payments(self) -> Amount:
        'Calculate the total amount of one-time payments in the period.'
        total = sum(payment.amount.value for payment in self._payments if payment.is_one_time_payment())
        return Amount(total)

    @property
    def total_last_payments(self) -> Amount:
        'Calculate the total amount of last payments in the period.'
        total = sum(payment.amount.value for payment in self._payments if payment.is_last_payment())
        return Amount(total)

    def add_payment(self, payment: Payment):
        'Add a payment to the period.'
        if not isinstance(payment, Payment):
            raise ValueError('payment must be an instance of Payment')
        self._payments.append(payment)

    def remove_payment(self, payment: Payment):
        'Remove a payment from the period.'
        if payment in self._payments:
            self._payments.remove(payment)
        else:
            raise ValueError('Payment not found in the period')
