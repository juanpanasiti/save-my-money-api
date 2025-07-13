from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from ...shared.base_entity import BaseEntity
from ...shared.value_objects.amount import Amount


class Account(BaseEntity, ABC):
    def __init__(
        self,
        alias: str,
        limit: Amount = Amount(0),
        is_enabled: bool = True,
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self._alias = alias
        self._limit = limit
        self._is_enabled = is_enabled

    @property
    def alias(self) -> str:
        'Get the alias of the account.'
        return self._alias

    @alias.setter
    def alias(self, value: str):
        'Set the alias of the account.'
        if not value:
            raise ValueError('Alias cannot be empty')
        self._alias = value

    @property
    def limit(self) -> Amount:
        'Get the limit of the account.'
        return self._limit

    @limit.setter
    def limit(self, value: Amount):
        'Set the limit of the account.'
        if value.value < 0:
            raise ValueError('Limit cannot be negative')
        self._limit = value

    @property
    def is_enabled(self) -> bool:
        'Check if the account is enabled.'
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value: bool):
        'Enable or disable the account.'
        if not isinstance(value, bool):
            raise ValueError('is_enabled must be a boolean value')
        self._is_enabled = value

    @property
    @abstractmethod
    def balance(self) -> Amount:
        'Get the current balance of the account.'
        ...
