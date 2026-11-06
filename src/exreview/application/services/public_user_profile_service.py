from math import ceil
from uuid import UUID

from exreview.application.ports.experience_repository import (
    ExperienceRepository,
)
from exreview.application.ports.user_repository import UserRepository
from exreview.domain.entities.experience import Experience
from exreview.domain.entities.user import User


class PublicUserProfileService:

    def __init__(
        self,
        user_repository: UserRepository,
        experience_repository: ExperienceRepository,
    ) -> None:
        self.user_repository = user_repository
        self.experience_repository = experience_repository

    def search(
        self,
        username: str,
        page: int,
        page_size: int,
    ) -> tuple[list[User], int]:

        if not username.strip():
            return [], 0

        return self.user_repository.search_by_username(
            username=username,
            page=page,
            page_size=page_size,
        )

    def get_profile(
        self,
        username: str,
    ) -> tuple[User, int] | None:

        user = self.user_repository.find_by_username(
            username.strip().lower()
        )

        if user is None or not user.is_active:
            return None

        published_count = (
            self.experience_repository.count_published_by_user(user.id)
        )

        return user, published_count

    def get_user_experiences(
        self,
        username: str,
        page: int,
        page_size: int,
    ) -> tuple[list[Experience], int] | None:

        user = self.user_repository.find_by_username(
            username.strip().lower()
        )

        if user is None or not user.is_active:
            return None

        return self.experience_repository.find_published_by_user(
            user_id=user.id,
            page=page,
            page_size=page_size,
        )

    @staticmethod
    def total_pages(total: int, page_size: int) -> int:
        return ceil(total / page_size) if total else 0