from ..models import Subscription
from .expense_repository_interface import ExpenseRepositoryInterface


class SubscriptionRepositoryInterface(ExpenseRepositoryInterface[Subscription]):
    ...
