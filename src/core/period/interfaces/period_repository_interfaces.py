from abc import abstractmethod
from typing import Optional

from ...shared.paginated_result import PaginatedResult
from ...shared.filter_base import FilterBase
from ...shared.interfaces.repository_base import RepositoryBase
from ..models import Period


class PeriodRepositoryInterface(RepositoryBase[Period]):
    @abstractmethod
    def get_all(
        self, page: int, page_size: int, filter: Optional[FilterBase] = None
    ) -> PaginatedResult[Period]:
        '''Get a paginated result of all periods, optionally filtered by a given filter.'''
        ...

    @abstractmethod
    def get_by_month_and_year(
        self, month: int, year: int, filter: Optional[FilterBase] = None
    ) -> Optional[Period]:
        '''Get a period by its month and year, optionally filtered by a given filter.'''
        ...
