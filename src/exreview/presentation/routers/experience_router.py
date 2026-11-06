from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from exreview.application.dto.requests.create_experience_request import (
    CreateExperienceRequest,
)
from exreview.application.services.create_experience_service import (
    CreateExperienceService,
)
from exreview.application.services.experience_query_service import (
    ExperienceQueryService,
)
from exreview.domain.entities.user import User
from exreview.presentation.dependencies.current_user_dependencies  import get_current_user
from exreview.presentation.dependencies.experience_dependencies import (
    get_create_experience_service,
    get_experience_query_service,
)
from exreview.presentation.schemas.requests.create_experience_schema import (
    CreateExperienceSchema,
)
from exreview.presentation.schemas.responses.experience_response_schema import (
    ExperienceListResponseSchema,
    ExperienceResponseSchema,
)

from fastapi import Response

from exreview.application.services.update_experience_service import (
    UpdateExperienceService,
)
from exreview.application.services.publish_experience_service import (
    PublishExperienceService,
)
from exreview.application.services.delete_experience_service import (
    DeleteExperienceService,
)
from exreview.presentation.dependencies.experience_dependencies import (
    get_update_experience_service,
    get_publish_experience_service,
    get_delete_experience_service,
)
from exreview.presentation.schemas.requests.update_experience_schema import (
    UpdateExperienceSchema,
)

router = APIRouter(
    prefix="/api/v1/experiences",
    tags=["Experiences"],
)


@router.post(
    "",
    response_model=ExperienceResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_experience(
    request: CreateExperienceSchema,
    current_user: User = Depends(get_current_user),
    service: CreateExperienceService = Depends(
        get_create_experience_service
    ),
):
    experience_request = CreateExperienceRequest(
        title=request.title,
        story=request.story,
        lesson=request.lesson,
        category=request.category,
        publish=request.publish,
    )

    experience = service.create(
        user_id=current_user.id,
        request=experience_request,
    )

    return experience


@router.get(
    "",
    response_model=ExperienceListResponseSchema,
)
def browse_experiences(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    service: ExperienceQueryService = Depends(
        get_experience_query_service
    ),
):
    experiences, total = service.get_published(page, page_size)

    return ExperienceListResponseSchema(
        items=experiences,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=service.total_pages(total, page_size),
    )


@router.get(
    "/me",
    response_model=ExperienceListResponseSchema,
)
def get_my_experiences(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    service: ExperienceQueryService = Depends(
        get_experience_query_service
    ),
):
    experiences, total = service.get_my_experiences(
        current_user.id,
        page,
        page_size,
    )

    return ExperienceListResponseSchema(
        items=experiences,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=service.total_pages(total, page_size),
    )


@router.get(
    "/{experience_id}",
    response_model=ExperienceResponseSchema,
)
def get_experience(
    experience_id: UUID,
    service: ExperienceQueryService = Depends(
        get_experience_query_service
    ),
):
    experience = service.get_published_by_id(experience_id)

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found.",
        )

    return experience

@router.put(
    "/{experience_id}",
    response_model=ExperienceResponseSchema,
)
def update_experience(
    experience_id: UUID,
    request: UpdateExperienceSchema,
    current_user: User = Depends(get_current_user),
    service: UpdateExperienceService = Depends(
        get_update_experience_service
    ),
):
    experience = service.update(
        experience_id=experience_id,
        user_id=current_user.id,
        title=request.title,
        story=request.story,
        lesson=request.lesson,
        category=request.category,
    )

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found.",
        )

    return experience


@router.patch(
    "/{experience_id}/publish",
    response_model=ExperienceResponseSchema,
)
def publish_experience(
    experience_id: UUID,
    current_user: User = Depends(get_current_user),
    service: PublishExperienceService = Depends(
        get_publish_experience_service
    ),
):
    experience = service.publish(
        experience_id=experience_id,
        user_id=current_user.id,
    )

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found.",
        )

    return experience


@router.delete(
    "/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_experience(
    experience_id: UUID,
    current_user: User = Depends(get_current_user),
    service: DeleteExperienceService = Depends(
        get_delete_experience_service
    ),
):
    deleted = service.delete(
        experience_id=experience_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

