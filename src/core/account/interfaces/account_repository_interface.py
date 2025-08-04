from abc import abstractmethod
from typing import Optional, Generic, TypeVar

from ...shared.paginated_result import PaginatedResult
from ...shared.filter_base import FilterBase
from ...shared.interfaces.repository_base import RepositoryBase

T = TypeVar('T')


class AccountRepositoryInterface(RepositoryBase[T], Generic[T]):
    @abstractmethod
    def get_by_owner_id(self, owner_id: str, filters: Optional[FilterBase] = None) -> PaginatedResult[T]:
        ...