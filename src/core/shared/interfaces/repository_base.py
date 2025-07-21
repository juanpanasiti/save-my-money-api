from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, Generic, TypeVar

from ..paginated_result import PaginatedResult
from ..filter_base import FilterBase

T = TypeVar('T')


class RepositoryBase(ABC, Generic[T]):
    @abstractmethod
    def get_paginated(self, page: int, page_size: int, filter: Optional[FilterBase] = None) -> PaginatedResult[T]:
        '''Get a paginated result of entities, optionally filtered by a given filter.'''
        ...

    @abstractmethod
    def get_one(self, id: UUID, filter: Optional[FilterBase] = None) -> Optional[T]:
        '''Get a single entity by its ID, optionally filtered by a given filter.'''
        ...

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[T]:
        '''Get an entity by its ID.'''
        ...

    @abstractmethod
    def save(self, entity: T) -> T:
        '''Save an entity, either creating or updating it based on its ID.'''
        ...

    @abstractmethod
    def delete(self, id: UUID) -> None:
        '''Delete an entity by its ID.'''
        ...

    @abstractmethod
    def count(self, filter: Optional[FilterBase] = None) -> int:
        '''Count the total number of entities, optionally filtered by a given filter.'''
        ...

    @abstractmethod
    def exists(self, id: UUID) -> bool:
        '''Check if an entity with the given ID exists.'''
        ...
