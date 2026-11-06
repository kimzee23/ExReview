from fastapi import Depends
from sqlalchemy.orm import Session

from exreview.application.services.create_experience_service import (
    CreateExperienceService,
)
from exreview.application.services.experience_query_service import (
    ExperienceQueryService,
)
from exreview.infrastructure.repositories.sqlalchemy_experience_repository import (
    SQLAlchemyExperienceRepository,
)
from exreview.infrastructure.database.connection import get_db

from exreview.application.services.update_experience_service import (
    UpdateExperienceService,
)
from exreview.application.services.publish_experience_service import (
    PublishExperienceService,
)
from exreview.application.services.delete_experience_service import (
    DeleteExperienceService,
)

def get_experience_repository(
    session: Session = Depends(get_db),
) -> SQLAlchemyExperienceRepository:
    return SQLAlchemyExperienceRepository(session)


def get_create_experience_service(
    repository: SQLAlchemyExperienceRepository = Depends(
        get_experience_repository
    ),
) -> CreateExperienceService:
    return CreateExperienceService(repository)


def get_experience_query_service(
    repository: SQLAlchemyExperienceRepository = Depends(
        get_experience_repository
    ),
) -> ExperienceQueryService:
    return ExperienceQueryService(repository)

def get_update_experience_service(
    repository: SQLAlchemyExperienceRepository = Depends(
        get_experience_repository
    ),
) -> UpdateExperienceService:
    return UpdateExperienceService(repository)


def get_publish_experience_service(
    repository: SQLAlchemyExperienceRepository = Depends(
        get_experience_repository
    ),
) -> PublishExperienceService:
    return PublishExperienceService(repository)


def get_delete_experience_service(
    repository: SQLAlchemyExperienceRepository = Depends(
        get_experience_repository
    ),
) -> DeleteExperienceService:
    return DeleteExperienceService(repository)