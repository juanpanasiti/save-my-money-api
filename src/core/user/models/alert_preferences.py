from uuid import UUID
from typing import Optional

from ...shared.entity_base import EntityBase
from ...shared.value_objects import Amount


class AlertPreferences(EntityBase):
    def __init__(
        self,
        profile_id: UUID,
        monthly_spending_limit: Amount = Amount(0),
        id: Optional[UUID] = None,
    ):
        super().__init__(id)
        self._profile_id = profile_id
        self._monthly_spending_limit = monthly_spending_limit

    @property
    def monthly_spending_limit(self) -> Amount:
        'Get the monthly spending limit.'
        return self._monthly_spending_limit

    @monthly_spending_limit.setter
    def monthly_spending_limit(self, value: Amount):
        'Set the monthly spending limit.'
        self._monthly_spending_limit = value

    @classmethod
    def from_dict(cls, data: dict) -> 'AlertPreferences':
        'Create an AlertPreferences instance from a dictionary.'
        return cls(
            profile_id=UUID(data.get('profile_id', '')),
            monthly_spending_limit=Amount(data.get('monthly_spending_limit', 0)),
            id=data.get('id')
        )
