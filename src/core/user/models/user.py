from uuid import UUID
from typing import Optional

from ...shared.entity_base import EntityBase
from ..enums import Role
from .profile import Profile


class User(EntityBase):
    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        role: Role = Role.FREE_USER,
        profile: Optional[Profile] = None,
        id: Optional[UUID] = None,
    ):
        super().__init__(id)
        self._username = username
        self._email = email
        self._password = password
        self._role = role
        self._profile = profile

    @property
    def username(self) -> str:
        'Get the username.'
        return self._username

    @property
    def email(self) -> str:
        'Get the email.'
        return self._email

    @property
    def password(self) -> str:
        'Get the password.'
        return self._password

    @password.setter
    def password(self, value: str):
        'Set the password.'
        self._password = value

    @property
    def role(self) -> Role:
        'Get the role.'
        return self._role

    @role.setter
    def role(self, value: Role):
        'Set the role.'
        self._role = value

    @property
    def profile(self) -> Profile:
        'Get the profile.'
        if self._profile is None:
            self._profile = Profile(user_id=self.id, first_name='', last_name='')
        return self._profile

    @profile.setter
    def profile(self, value: Profile):
        'Set the profile.'
        self._profile = value


    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        'Create a User instance from a dictionary.'
        return cls(
            username=data.get('username', ''),
            email=data.get('email', ''),
            password=data.get('password', ''),
            role=Role(data.get('role', Role.FREE_USER.value)),
            profile=Profile.from_dict(data.get('profile', {})),
            id=data.get('id')
        )