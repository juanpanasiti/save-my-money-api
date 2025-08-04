from abc import abstractmethod
from typing import List
from uuid import UUID

from ...shared.interfaces.repository_base import RepositoryBase
from ..models import ExpenseCategory


class ExpenseCategoryRepositoryInterface(RepositoryBase[ExpenseCategory]):
    @abstractmethod
    def get_by_owner_id(self, owner_id: UUID) -> List[ExpenseCategory]:
        '''Get all expense categories for a specific owner by their ID.'''
        ...

    @abstractmethod
    def get_by_income_type(self, is_income: bool) -> List[ExpenseCategory]:
        '''Get all expense categories filtered by whether they are for income or not.'''
        ...
