from abc import abstractmethod
from typing import Optional

from ...shared.paginated_result import PaginatedResult
from ...shared.filter_base import FilterBase
from ...shared.interfaces.repository_base import RepositoryBase

from ..models import User, Profile, AlertPreferences


class UserRepositoryInterface(RepositoryBase[User]):
    @abstractmethod
    def get_by_email(self, email: str, filter: Optional[FilterBase] = None) -> Optional[User]:
        '''Get a user by their email address, optionally filtered by a given filter.'''
        ...

    @abstractmethod
    def get_by_username(self, username: str, filter: Optional[FilterBase] = None) -> Optional[User]:
        '''Get a user by their username, optionally filtered by a given filter.'''
        ...

    @abstractmethod
    def get_users_by_role(
        self, role: str, page: int, page_size: int, filter: Optional[FilterBase] = None
    ) -> PaginatedResult[User]:
        '''Get a paginated result of users by their role, optionally filtered by a given filter.'''
        ...

    @abstractmethod
    def update_user_role(self, user_id: str, new_role: str) -> User:
        '''Update the role of a user by their ID.'''
        ...

    @abstractmethod
    def update_profile(self, user_id: str, profile_data: dict) -> Profile:
        '''Update the profile of a user by their ID.'''
        ...

    @abstractmethod
    def get_profile(self, user_id: str) -> Optional[Profile]:
        '''Get the profile of a user by their ID.'''
        ...

    @abstractmethod
    def get_alert_preferences(self, user_id: str) -> AlertPreferences:
        '''Get the alert preferences of a user by their ID.'''
        ...

    @abstractmethod
    def update_alert_preferences(self, user_id: str, preferences_data: dict) -> AlertPreferences:
        '''Update the alert preferences of a user by their ID.'''
        ...
