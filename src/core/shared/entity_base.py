
from uuid import UUID, uuid4
from typing import Optional
from abc import ABC, abstractmethod


class EntityBase(ABC):
    def __init__(self, id: Optional[UUID] = None):
        self.id = id if id is not None else uuid4()

    def to_dict(self) -> dict:
        '''Convert the entity to a dictionary representation.'''
        return self.__dict__

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict)-> 'EntityBase':
        '''Create an entity instance from a dictionary representation.'''
        ...