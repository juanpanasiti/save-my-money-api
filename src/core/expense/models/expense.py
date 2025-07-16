from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from datetime import date
from typing import List

from ...shared.entity_base import EntityBase
from ...shared.value_objects import Amount
from ...account.models.account import Account
from ..exceptions import ExpenseStatusException
from ..enums import ExpenseType, ExpenseStatus
from .expense_category import ExpenseCategory as Category
from .payment import Payment


class Expense(EntityBase, ABC):
    VALID_STATUS = {ExpenseStatus.ACTIVE, ExpenseStatus.PENDING, ExpenseStatus.FINISHED, ExpenseStatus.CANCELLED}

    def __init__(
        self,
        account: Account,
        title: str,
        cc_name: str,
        acquired_at: date,
        amount: Amount,
        expense_type: ExpenseType,
        installments: int = 1,
        first_payment_date: Optional[date] = None,
        status: ExpenseStatus = ExpenseStatus.ACTIVE,
        category: Optional[Category] = None,
        payments: List[Payment] = [],
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self._account = account
        self._title = title
        self._cc_name = cc_name
        self._acquired_at = acquired_at
        self._amount = amount
        self._expense_type = expense_type
        self._installments = installments
        self._first_payment_date = first_payment_date
        self._status = status
        self._category = category
        self._payments = payments if payments is not None else []

    @property
    def account(self) -> Account:
        'Get the account associated with the expense.'
        return self._account

    @account.setter
    def account(self, value: Account):
        'Set the account associated with the expense.'
        self._account = value

    @property
    def title(self) -> str:
        'Get the title of the expense.'
        return self._title

    @title.setter
    def title(self, value: str):
        'Set the title of the expense.'
        self._title = value

    @property
    def cc_name(self) -> str:
        'Get the credit card name.'
        return self._cc_name

    @cc_name.setter
    def cc_name(self, value: str):
        'Set the credit card name.'
        self._cc_name = value

    @property
    def acquired_at(self) -> date:
        'Get the acquisition date.'
        return self._acquired_at

    @acquired_at.setter
    def acquired_at(self, value: date):
        'Set the acquisition date.'
        self._acquired_at = value

    @property
    def amount(self) -> Amount:
        'Get the amount of the expense.'
        return self._amount

    @amount.setter
    def amount(self, value: Amount):
        'Set the amount of the expense.'
        self._amount = value

    @property
    def expense_type(self) -> ExpenseType:
        'Get the type of the expense.'
        return self._expense_type

    @expense_type.setter
    def expense_type(self, value: ExpenseType):
        'Set the type of the expense.'
        self._expense_type = value

    @property
    def installments(self) -> int:
        'Get the number of installments.'
        return self._installments

    @installments.setter
    def installments(self, value: int):
        'Set the number of installments.'
        self._installments = value

    @property
    def first_payment_date(self) -> Optional[date]:
        'Get the first payment date.'
        return self._first_payment_date

    @first_payment_date.setter
    def first_payment_date(self, value: Optional[date]):
        'Set the first payment date.'
        self._first_payment_date = value

    @property
    def status(self) -> ExpenseStatus:
        'Get the status of the expense.'
        return self._status

    @status.setter
    def status(self, value: ExpenseStatus):
        'Set the status of the expense.'
        if value not in self.VALID_STATUS:
            raise ExpenseStatusException(f'Status must be one of {self.VALID_STATUS}')
        self._status = value

    @property
    def category_id(self) -> object:
        'Get the category id.'
        return self._category

    @category_id.setter
    def category_id(self, value: object):
        'Set the category id.'
        self._category = value

    @property
    def payments(self) -> List[Payment]:
        'Get the payments list.'
        return self._payments

    @payments.setter
    def payments(self, value: List[Payment]):
        'Set the payments list.'
        self._payments = value

    @abstractmethod
    def calculate_payments(self) -> None:
        'Calculate the payments based on the expense details.'
        ...

    @property
    @abstractmethod
    def pending_amount(self) -> Amount:
        'Calculate the pending amount of the expense.'
        ...

    @property
    @abstractmethod
    def pending_financing_amount(self) -> Amount:
        'Calculate the pending financing amount of the expense.'
        ...

    @property
    def total_pending_amount(self) -> Amount:
        'Calculate the total pending amount of the expense.'
        return self.pending_amount + self.pending_financing_amount