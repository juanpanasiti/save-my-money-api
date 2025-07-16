from uuid import UUID
from typing import Optional
from datetime import date
from typing import List

from ...shared.helpers.dates import add_months_to_date
from ...shared.value_objects import Amount
from ...account.models.account import Account
from ..exceptions import PaymentNotFoundInExpenseException
from ..enums import ExpenseType, ExpenseStatus, PaymentStatus
from .expense import Expense
from .expense_category import ExpenseCategory as Category
from .payment import Payment


class Subscription(Expense):
    VALID_STATUS = {ExpenseStatus.ACTIVE, ExpenseStatus.CANCELLED}

    def __init__(
        self,
        account: Account,
        title: str,
        cc_name: str,
        acquired_at: date,
        amount: Amount,
        first_payment_date: Optional[date] = None,
        category: Optional[Category] = None,
        payments: List[Payment] = [],
        id: Optional[UUID] = None
    ):
        super().__init__(
            account,
            title,
            cc_name,
            acquired_at,
            amount,
            ExpenseType.SUBSCRIPTION,
            1,  # Subscriptions typically have one installment at the beginning
            first_payment_date,
            ExpenseStatus.ACTIVE,
            category,
            payments,
            id
        )
        if not payments:
            self.calculate_payments()

    @property
    def pending_amount(self) -> Amount:
        'Calculate the pending amount of the subscription.'
        total_pending = sum(payment.amount.value for payment in self._payments if payment.status == PaymentStatus.CONFIRMED)
        return Amount(total_pending)

    @property
    def pending_financing_amount(self) -> Amount:
        'A suscription has not financing amounts.'
        return Amount(0)

    def calculate_payments(self) -> None:
        payment = Payment(
            expense=self,
            amount=self._amount,
            no_installment=1,
            status=PaymentStatus.UNCONFIRMED,
            payment_date=self._first_payment_date
        )
        self._payments.append(payment)

    def add_new_payment(self, payment: Payment) -> None:
        if payment.expense.id != self.id:
            raise ValueError('Payment expense ID does not match subscription ID')
        self._amount = payment.amount
        self._payments.append(payment)
        self.__sort_payments_by_date()
        self.__update_amount()

    def remove_payment(self, payment_id: UUID) -> None:
        for payment in self._payments:
            if payment.id == payment_id:
                self._payments.remove(payment)
                self.__sort_payments_by_date()
                self.__update_amount()
                return
        raise PaymentNotFoundInExpenseException(f'Payment with ID {payment_id} not found in subscription {self.title}.')

    def update_payment(self, payment_id: UUID, payment: Payment) -> None:
        for i, payment in enumerate(self._payments):
            if payment.id == payment_id:
                self._payments[i] = payment
                self.__sort_payments_by_date()
                self.__update_amount()
                return
        raise PaymentNotFoundInExpenseException(f'Payment with ID {payment_id} not found in subscription {self.title}.')

    def get_next_payment(self, factor: Amount = Amount(1.0), is_simulated: bool = False) -> Payment:
        if factor.value <= 0:
            raise ValueError('Factor must be greater than zero')
        last_payment_date = self._payments[-1].payment_date if self._payments else None
        next_payment_date = add_months_to_date(last_payment_date, 1) if last_payment_date else self._acquired_at
        return Payment(
            expense=self,
            amount=Amount(self._amount.value * factor.value),
            no_installment=len(self._payments) + 1,
            status=PaymentStatus.SIMULATED if is_simulated else PaymentStatus.UNCONFIRMED,
            payment_date=next_payment_date
        )

    def __sort_payments_by_date(self) -> None:
        self._payments.sort(key=lambda p: p.payment_date if p.payment_date else date.min)
        for i, payment in enumerate(self._payments, start=1):
            if payment.no_installment != i:
                payment.no_installment = i

    def __update_amount(self) -> None:
        '''Update amount if the last payment amount changed.'''
        last_payment = self._payments[-1] if self._payments else None
        if last_payment and last_payment.amount != self._amount:
            self._amount = last_payment.amount

    @classmethod
    def from_dict(cls, data: dict) -> 'Subscription':
        '''Create a Subscription instance from a dictionary representation.'''
        payments = [Payment.from_dict(payment) for payment in data.get('payments', [])]
        return cls(
            account=data['account'],
            title=data['title'],
            cc_name=data['cc_name'],
            acquired_at=data['acquired_at'],
            amount=Amount(data['amount']),
            first_payment_date=data.get('first_payment_date'),
            category=data.get('category'),
            payments=payments,
            id=data.get('id')
        )
