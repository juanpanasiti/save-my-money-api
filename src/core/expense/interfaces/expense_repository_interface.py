from abc import abstractmethod
from typing import Optional, Generic, TypeVar
from uuid import UUID

from ...shared.paginated_result import PaginatedResult
from ...shared.filter_base import FilterBase
from ...shared.interfaces.repository_base import RepositoryBase
from ..models import Expense

T = TypeVar('T', bound=Expense)


class ExpenseRepositoryInterface(RepositoryBase[T], Generic[T]):
    @abstractmethod
    def get_by_account_ids(
        self, account_ids: list[UUID], page: int, page_size: int, filter: Optional[FilterBase] = None
    ) -> PaginatedResult[T]:
        '''Get a paginated result of expenses by account IDs, optionally filtered by a given filter.'''
        ...
