
from uuid import UUID, uuid4
from typing import Optional
from abc import ABC, abstractmethod


class BaseEntity(ABC):
    def __init__(self, id: Optional[UUID] = uuid4()):
        self.id = id

    @abstractmethod
    def to_dict(self) -> dict:
        'Serialize the entity into a dict.'
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        'Create an entity instance from a dict.'
        pass
