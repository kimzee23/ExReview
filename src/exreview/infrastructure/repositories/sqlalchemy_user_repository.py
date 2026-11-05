from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from exreview.application.ports.user_repository import UserRepository
from exreview.domain.entities.user import User
from exreview.infrastructure.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, user: User) -> User:
        existing_user = self.session.get(UserModel, user.id)

        if existing_user is None:
            existing_user = UserModel(id=user.id)
            self.session.add(existing_user)

        existing_user.email = user.email
        existing_user.password_hash = user.password_hash
        existing_user.display_name = user.display_name
        existing_user.is_active = user.is_active
        existing_user.created_at = user.created_at

        self.session.commit()
        self.session.refresh(existing_user)

        return self._to_entity(existing_user)

    def find_by_id(self, user_id: UUID) -> User | None:
        statement = select(UserModel).where(
            UserModel.id == user_id
        )

        user_model = self.session.scalar(statement)

        if user_model is None:
            return None

        return self._to_entity(user_model)

    def find_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(
            UserModel.email == email
        )

        user_model = self.session.scalar(statement)

        if user_model is None:
            return None

        return self._to_entity(user_model)

    @staticmethod
    def _to_entity(user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            email=user_model.email,
            password_hash=user_model.password_hash,
            display_name=user_model.display_name,
            is_active=user_model.is_active,
            created_at=user_model.created_at
        )