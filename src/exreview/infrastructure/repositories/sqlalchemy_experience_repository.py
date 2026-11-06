from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from exreview.application.ports.experience_repository import (
    ExperienceRepository,
)
from exreview.domain.entities.experience import Experience
from exreview.domain.enums.experience_category import ExperienceCategory
from exreview.domain.enums.experience_status import ExperienceStatus
from exreview.infrastructure.models.experience_model import ExperienceModel


class SQLAlchemyExperienceRepository(ExperienceRepository):

    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _to_entity(model: ExperienceModel) -> Experience:
        return Experience(
            id=model.id,
            user_id=model.user_id,
            title=model.title,
            story=model.story,
            lesson=model.lesson,
            category=ExperienceCategory(model.category),
            status=ExperienceStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def save(self, experience: Experience) -> Experience:
        model = self.session.get(ExperienceModel, experience.id)

        if model is None:
            model = ExperienceModel(
                id=experience.id,
                user_id=experience.user_id,
                title=experience.title,
                story=experience.story,
                lesson=experience.lesson,
                category=experience.category.value,
                status=experience.status.value,
            )
            self.session.add(model)
        else:
            model.title = experience.title
            model.story = experience.story
            model.lesson = experience.lesson
            model.category = experience.category.value
            model.status = experience.status.value

        try:
            self.session.commit()
            self.session.refresh(model)
            return self._to_entity(model)
        except Exception:
            self.session.rollback()
            raise

    def find_by_id(self, experience_id: UUID) -> Experience | None:
        model = self.session.get(ExperienceModel, experience_id)

        return self._to_entity(model) if model else None

    def find_by_id_and_user(
        self,
        experience_id: UUID,
        user_id: UUID,
    ) -> Experience | None:
        model = self.session.scalar(
            select(ExperienceModel).where(
                ExperienceModel.id == experience_id,
                ExperienceModel.user_id == user_id,
            )
        )

        return self._to_entity(model) if model else None

    def find_published(
        self,
        page: int,
        page_size: int,
    ) -> tuple[list[Experience], int]:
        conditions = (
            ExperienceModel.status == ExperienceStatus.PUBLISHED.value,
        )

        statement = (
            select(ExperienceModel)
            .where(*conditions)
            .order_by(ExperienceModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        count_statement = (
            select(func.count())
            .select_from(ExperienceModel)
            .where(*conditions)
        )

        models = self.session.scalars(statement).all()
        total = self.session.scalar(count_statement) or 0

        return [self._to_entity(model) for model in models], total

    def find_by_user(
        self,
        user_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[Experience], int]:
        conditions = (ExperienceModel.user_id == user_id,)

        statement = (
            select(ExperienceModel)
            .where(*conditions)
            .order_by(ExperienceModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        count_statement = (
            select(func.count())
            .select_from(ExperienceModel)
            .where(*conditions)
        )

        models = self.session.scalars(statement).all()
        total = self.session.scalar(count_statement) or 0

        return [self._to_entity(model) for model in models], total

    def delete(self, experience_id: UUID) -> None:
        model = self.session.get(ExperienceModel, experience_id)

        if model is not None:
            try:
                self.session.delete(model)
                self.session.commit()
            except Exception:
                self.session.rollback()
                raise

    def find_published_by_user(
            self,
            user_id: UUID,
            page: int,
            page_size: int,
    ) -> tuple[list[Experience], int]:

        conditions = (
            ExperienceModel.user_id == user_id,
            ExperienceModel.status == ExperienceStatus.PUBLISHED.value,
        )

        statement = (
            select(ExperienceModel)
            .where(*conditions)
            .order_by(ExperienceModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        count_statement = (
            select(func.count())
            .select_from(ExperienceModel)
            .where(*conditions)
        )

        models = self.session.scalars(statement).all()
        total = self.session.scalar(count_statement) or 0

        return [self._to_entity(model) for model in models], total

    def count_published_by_user(self, user_id: UUID) -> int:

        statement = (
            select(func.count())
            .select_from(ExperienceModel)
            .where(
                ExperienceModel.user_id == user_id,
                ExperienceModel.status == ExperienceStatus.PUBLISHED.value,
            )
        )

        return self.session.scalar(statement) or 0