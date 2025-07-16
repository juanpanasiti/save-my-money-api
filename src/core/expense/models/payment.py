from uuid import UUID
from typing import Optional
from datetime import date

from ...shared.entity_base import EntityBase
from ...shared.value_objects import Amount
from ..enums import PaymentStatus
from expense import Expense


class Payment(EntityBase):
    def __init__(
            self,
            expense: Expense,
            amount: Amount,
            no_installment: int,
            status: PaymentStatus = PaymentStatus.UNCONFIRMED,
            payment_date: Optional[date] = None,
            id: Optional[UUID] = None
    ) -> None:
        super().__init__(id)
        self._expense = expense
        self._amount = amount
        self._no_installment = no_installment
        self._status = status
        self._payment_date = payment_date

    @property
    def expense(self) -> Expense:
        'Get the associated expense for this payment.'
        return self._expense

    @expense.setter
    def expense(self, value: Expense):
        'Set the associated expense for this payment.'
        if not isinstance(value, Expense):
            raise ValueError('expense must be an instance of Expense')
        self._expense = value

    @property
    def amount(self) -> Amount:
        'Get the payment amount.'
        return self._amount

    @amount.setter
    def amount(self, value: Amount):
        'Set the payment amount.'
        self._amount = value

    @property
    def no_installment(self) -> int:
        'Get the installment number.'
        return self._no_installment

    @no_installment.setter
    def no_installment(self, value: int):
        'Set the installment number.'
        self._no_installment = value

    @property
    def status(self) -> PaymentStatus:
        'Get the payment status.'
        return self._status

    @status.setter
    def status(self, value: PaymentStatus):
        'Set the payment status.'
        self._status = value

    @property
    def payment_date(self) -> Optional[date]:
        'Get the payment date.'
        return self._payment_date

    @payment_date.setter
    def payment_date(self, value: date):
        'Set the payment date.'
        self._payment_date = value

    def is_final_status(self) -> bool:
        'Check if the payment status is final.'
        return self._status in {PaymentStatus.PAID, PaymentStatus.CANCELED}

    @classmethod
    def from_dict(cls, data: dict) -> 'Payment':
        '''Create a Payment instance from a dictionary representation.'''
        expense = data.get('expense')
        if not isinstance(expense, Expense):
            raise ValueError('expense must be an instance of Expense')
        return cls(
            expense=expense,
            amount=Amount(data['amount']),
            no_installment=data['no_installment'],
            status=PaymentStatus(data['status']),
            payment_date=data.get('payment_date'),
            id=data.get('id')
        )
