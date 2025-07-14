from uuid import UUID
from typing import Optional

from ...shared.entity_base import EntityBase


class ExpenseCategory(EntityBase):
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        is_income: bool = False,
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self._name = name
        self._description = description
        self._is_income = is_income

    @property
    def name(self) -> str:
        'Get the name of the expense category.'
        return self._name

    @name.setter
    def name(self, value: str):
        'Set the name of the expense category.'
        if not value:
            raise ValueError('Name cannot be empty')
        self._name = value

    @property
    def description(self) -> Optional[str]:
        'Get the description of the expense category.'
        return self._description

    @description.setter
    def description(self, value: Optional[str]):
        'Set the description of the expense category.'
        self._description = value
    
    @property
    def is_income(self) -> bool:
        'Check if the category is for income.'
        return self._is_income
    @is_income.setter
    def is_income(self, value: bool):
        'Set whether the category is for income.'
        if not isinstance(value, bool):
            raise ValueError('is_income must be a boolean value')
        self._is_income = value