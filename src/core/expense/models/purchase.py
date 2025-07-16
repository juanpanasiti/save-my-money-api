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


class Purchase(Expense):
    VALID_STATUS = {ExpenseStatus.PENDING, ExpenseStatus.FINISHED}

    def __init__(
        self,
        account: Account,
        title: str,
        cc_name: str,
        acquired_at: date,
        amount: Amount,
        installments: int = 1,
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
            ExpenseType.PURCHASE,
            installments,
            first_payment_date,
            ExpenseStatus.PENDING,
            category,
            payments,
            id
        )
        if not payments:
            self.calculate_payments()

    @property
    def paid_amount(self) -> Amount:
        'Calculate the total amount paid for the purchase.'
        total_paid = sum(payment.amount.value for payment in self._payments if payment.is_final_status())
        return Amount(total_paid)

    @property
    def pending_installments(self) -> int:
        'Calculate the number of pending installments.'
        return len([payment for payment in self._payments if not payment.is_final_status()])

    @property
    def done_installments(self) -> int:
        'Calculate the number of installments that have been paid.'
        return len([payment for payment in self._payments if payment.is_final_status()])

    @property
    def pending_financing_amount(self) -> Amount:
        '''Calculate the pending financing amount of the purchase.'''
        total_financing = Amount(0)
        if self._installments == 1:
            # If there is only one installment, there is no financing
            return total_financing
        for payment in self._payments:
            if not payment.is_final_status():
                total_financing += payment.amount
        return total_financing

    @property
    def pending_amount(self) -> Amount:
        'Calculate the pending amount of the purchase made in one payment.'
        if self._installments > 1:
            return Amount(0)
        # If the purchase has only one installment and it is not a final status, return the total amount
        if self._payments[0].is_final_status():
            return Amount(0)
        return self._amount

    def calculate_payments(self) -> None:
        remaining_amount = self._amount.value
        remaining_installments = self._installments
        payment_date: date = self._first_payment_date or self._acquired_at
        for no in range(1, self._installments + 1):
            installment_amount = Amount(remaining_amount / remaining_installments)
            payment = Payment(
                expense=self,
                amount=installment_amount,
                no_installment=no,
                status=PaymentStatus.UNCONFIRMED,
                payment_date=payment_date
            )
            self._payments.append(payment)
            remaining_amount -= installment_amount.value
            remaining_installments -= 1
            payment_date = add_months_to_date(payment_date, 1) if self._installments > 1 else payment_date

    def update_status(self) -> None:
        'Update the status of the purchase based on current conditions.'
        if any(not payment.is_final_status() for payment in self._payments):
            self._status = ExpenseStatus.PENDING
        else:
            self._status = ExpenseStatus.FINISHED

    def update_payment(self, payment: Payment) -> None:
        'Update a specific payment and adjust the purchase status and unconfirmed payment amounts accordingly.'
        payment_to_update = next((p for p in self._payments if p.id == payment.id), None)
        if not payment_to_update:
            raise PaymentNotFoundInExpenseException(f'Payment with id {payment.id} not found in purchase.')

        payment_to_update.amount = payment.amount
        payment_to_update.status = payment.status

        pending_payments = [p for p in self._payments if not p.is_final_status()]
        if not pending_payments:
            self.update_status()
            return

        pendig_amount = self.pending_amount
        if all(payment.status == PaymentStatus.CONFIRMED for payment in pending_payments):
            self.amount = Amount(sum(payment.amount.value for payment in pending_payments))
            return

        for payment in pending_payments:
            if payment.status == PaymentStatus.CONFIRMED:
                continue
            else:
                payment.amount = Amount(pendig_amount.value / len(pending_payments))
                pendig_amount = Amount(pendig_amount.value - payment.amount.value)

    @classmethod
    def from_dict(cls, data: dict) -> 'Purchase':
        '''Create a Purchase instance from a dictionary representation.'''
        payments = [Payment.from_dict(payment) for payment in data.get('payments', [])]
        return cls(
            account=data['account'],
            title=data['title'],
            cc_name=data['cc_name'],
            acquired_at=data['acquired_at'],
            amount=Amount(data['amount']),
            installments=data.get('installments', 1),
            first_payment_date=data.get('first_payment_date'),
            category=data.get('category'),
            payments=payments,
            id=data.get('id')
        )
