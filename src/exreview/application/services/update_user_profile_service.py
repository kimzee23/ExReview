from uuid import UUID

from exreview.application.ports.user_repository import UserRepository
from exreview.domain.entities.user import User
from exreview.domain.exceptions.username_already_exists_error import (
    UsernameAlreadyExistsError,
)


class UpdateUserProfileService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(
        self,
        user_id: UUID,
        username: str | None = None,
        display_name: str | None = None,
    ) -> User:

        if username is None and display_name is None:
            raise ValueError("Provide at least one profile field to update.")

        user = self.user_repository.find_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        if username is not None and username != user.username:
            existing_user = self.user_repository.find_by_username(username)

            if existing_user is not None and existing_user.id != user.id:
                raise UsernameAlreadyExistsError()

            user.username = username

        if display_name is not None:
            user.display_name = display_name

        return self.user_repository.save(user)