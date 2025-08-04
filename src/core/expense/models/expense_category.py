from uuid import UUID
from typing import Optional

from ...shared.entity_base import EntityBase
from ...user import User


class ExpenseCategory(EntityBase):
    def __init__(
        self,
        owner: User,
        name: str,
        description: Optional[str] = None,
        is_income: bool = False,
        id: Optional[UUID] = None
    ):
        super().__init__(id)
        self._name = name
        self._description = description
        self._is_income = is_income
        self._owner_id = owner.id

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

    @property
    def owner_id(self) -> UUID:
        'Get the ID of the owner of the expense category.'
        return self._owner_id

    @classmethod
    def from_dict(cls, data: dict) -> 'ExpenseCategory':
        '''Create an ExpenseCategory instance from a dictionary representation.'''
        return cls(
            name=data['name'],
            owner=User(**data['owner']),
            description=data.get('description'),
            is_income=data.get('is_income', False),
            id=data.get('id')
        )
