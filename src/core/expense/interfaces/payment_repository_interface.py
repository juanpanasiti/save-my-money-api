from abc import abstractmethod
from typing import Optional
from uuid import UUID

from ...shared.paginated_result import PaginatedResult
from ...shared.filter_base import FilterBase
from ...shared.interfaces.repository_base import RepositoryBase
from ..models import Payment


class PaymentRepositoryInterface(RepositoryBase[Payment]):
    @abstractmethod
    def get_by_expense_id(
        self, expense_id: UUID, page: int, page_size: int, filter: Optional[FilterBase] = None
    ) -> PaginatedResult[Payment]:
        '''Get a paginated result of payments by expense ID, optionally filtered by a given filter.'''
        ...

    @abstractmethod
    def get_by_date_range(
        self, start_date: str, end_date: str, page: int, page_size: int, filter: Optional[FilterBase] = None
    ) -> PaginatedResult[Payment]:
        '''Get a paginated result of payments within a date range, optionally filtered by a given filter.'''
        ...
