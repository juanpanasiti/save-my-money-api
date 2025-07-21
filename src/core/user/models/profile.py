from uuid import UUID
from typing import Optional
from datetime import date

from ...shared.entity_base import EntityBase
from .alert_preferences import AlertPreferences


class Profile(EntityBase):
    def __init__(
        self,
        user_id: UUID,
        first_name: str,
        last_name: str,
        birth_date: Optional[date] = None,
        alert_preferences: Optional[AlertPreferences] = None,
        id: Optional[UUID] = None,
    ):
        super().__init__(id)
        self._user_id = user_id
        self._first_name = first_name
        self._last_name = last_name
        self._birth_date = birth_date
        self._alert_preferences = alert_preferences

    @property
    def first_name(self) -> str:
        'Get the first name.'
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        'Set the first name.'
        self._first_name = value

    @property
    def last_name(self) -> str:
        'Get the last name.'
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        'Set the last name.'
        self._last_name = value

    @property
    def birth_date(self) -> Optional[date]:
        'Get the birth date.'
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value: date):
        'Set the birth date.'
        if value is not None and not isinstance(value, date):
            raise ValueError('birth_date must be a date instance')
        if value is not None and value > date.today():
            raise ValueError('birth_date cannot be in the future')
        self._birth_date = value

    @property
    def alert_preferences(self) -> AlertPreferences:
        'Get the alert preferences.'
        if self._alert_preferences is None:
            self._alert_preferences = AlertPreferences(profile_id=self.id)
        return self._alert_preferences

    @alert_preferences.setter
    def alert_preferences(self, value: Optional[AlertPreferences]):
        'Set the alert preferences.'
        self._alert_preferences = value


    @classmethod
    def from_dict(cls, data: dict) -> 'Profile':
        'Create a Profile instance from a dictionary.'
        return cls(
            user_id=UUID(data.get('user_id', '')),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            birth_date=data.get('birth_date'),
            alert_preferences=AlertPreferences.from_dict(data.get('alert_preferences', {})),
            id=data.get('id')
        )