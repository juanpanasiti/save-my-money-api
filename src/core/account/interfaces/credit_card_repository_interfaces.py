from ..models import CreditCard
from .account_repository_interface import AccountRepositoryInterface


class CreditCardRepositoryInterface(AccountRepositoryInterface[CreditCard]):
    ...
