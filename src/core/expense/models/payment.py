from uuid import UUID
from typing import Optional
from datetime import date

from ...shared.entity_base import EntityBase
from ...shared.value_objects import Amount
from ..enums import PaymentStatus


class Payment(EntityBase):
    def __init__(
            self,
            amount: Amount,
            no_installment: int,
            status: PaymentStatus = PaymentStatus.UNCONFIRMED,
            payment_date: Optional[date] = None,
            id: Optional[UUID] = None
    ) -> None:
        super().__init__(id)
        self._amount = amount
        self._no_installment = no_installment
        self._status = status
        self._payment_date = payment_date

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
