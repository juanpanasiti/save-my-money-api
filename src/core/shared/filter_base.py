from abc import ABC, abstractmethod

class FilterBase(ABC):
    @abstractmethod
    def get(self) -> dict:
        '''Return filter parameters as a dictionary.'''
        ...
