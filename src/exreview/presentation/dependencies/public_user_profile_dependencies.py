from fastapi import Depends
from sqlalchemy.orm import Session

from exreview.application.services.public_user_profile_service import (
    PublicUserProfileService,
)
from exreview.infrastructure.repositories.sqlalchemy_experience_repository import (
    SQLAlchemyExperienceRepository,
)
from exreview.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from exreview.application.services.update_user_profile_service import (
    UpdateUserProfileService,
)
from exreview.infrastructure.database.connection import get_db


def get_public_user_profile_service(
    session: Session = Depends(get_db),
) -> PublicUserProfileService:

    return PublicUserProfileService(
        user_repository=SQLAlchemyUserRepository(session),
        experience_repository=SQLAlchemyExperienceRepository(session),
    )

def get_update_user_profile_service(
    session: Session = Depends(get_db),
) -> UpdateUserProfileService:
    return UpdateUserProfileService(
        user_repository=SQLAlchemyUserRepository(session)
    )