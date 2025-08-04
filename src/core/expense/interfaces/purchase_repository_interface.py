from ..models import Purchase
from .expense_repository_interface import ExpenseRepositoryInterface


class PurchaseRepositoryInterface(ExpenseRepositoryInterface[Purchase]):
    ...
