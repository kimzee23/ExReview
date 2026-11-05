from fastapi import APIRouter, Depends, status

from exreview.application.dto.requests.register_user_request import (
    RegisterUserRequest,
)
from exreview.application.services.register_user_service import (
    RegisterUserService,
)
from exreview.presentation.dependencies.register_user_dependencies import (
    get_register_user_service,
)
from exreview.presentation.schemas.requests.register_user_request_schema import (
    RegisterUserRequestSchema,
)
from exreview.presentation.schemas.responses.register_user_response_schema import (
    RegisterUserResponseSchema,
)
from exreview.application.dto.requests.login_user_request import (
    LoginUserRequest,
)
from exreview.application.services.login_user_service import LoginUserService
from exreview.presentation.dependencies.auth_dependencies import (
    get_login_user_service,
)
from exreview.presentation.schemas.requests.login_user_request_schema import (
    LoginUserRequestSchema,
)
from exreview.presentation.schemas.responses.login_user_response_schema import (
    LoginUserResponseSchema,
)
from fastapi import Depends

from exreview.domain.entities.user import User
from exreview.presentation.dependencies.current_user_dependencies import (
    get_current_user,
)

from exreview.application.dto.requests.refresh_token_request import (
    RefreshTokenRequest,
)
from exreview.application.services.refresh_token_service import (
    RefreshTokenService,
)
from exreview.application.services.logout_user_service import (
    LogoutUserService,
)
from exreview.presentation.dependencies.auth_dependencies import (
    get_refresh_token_service,
    get_logout_user_service,
)
from exreview.presentation.schemas.requests.refresh_token_request_schema import (
    RefreshTokenRequestSchema,
)
from exreview.presentation.schemas.requests.logout_request_schema import (
    LogoutRequestSchema,
)


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=RegisterUserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    request: RegisterUserRequestSchema,
    service: RegisterUserService = Depends(get_register_user_service),
) -> RegisterUserResponseSchema:

    registration_request = RegisterUserRequest(
        email=str(request.email),
        password=request.password,
        display_name=request.display_name,
    )

    response = service.register(registration_request)

    return RegisterUserResponseSchema.model_validate(response)

@router.post(
    "/login",
    response_model=LoginUserResponseSchema,
)
def login_user(
    request: LoginUserRequestSchema,
    service: LoginUserService = Depends(get_login_user_service),
) -> LoginUserResponseSchema:

    login_request = LoginUserRequest(
        email=str(request.email),
        password=request.password,
    )

    response = service.login(login_request)

    return LoginUserResponseSchema.model_validate(response)

@router.get(
    "/me",
    response_model=RegisterUserResponseSchema,
)
def get_authenticated_user(
    current_user: User = Depends(get_current_user),
) -> RegisterUserResponseSchema:

    return RegisterUserResponseSchema(
        id=current_user.id,
        email=current_user.email,
        display_name=current_user.display_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
    )


@router.post(
    "/refresh",
    response_model=LoginUserResponseSchema,
)
def refresh_tokens(
    request: RefreshTokenRequestSchema,
    service: RefreshTokenService = Depends(get_refresh_token_service),
) -> LoginUserResponseSchema:

    refresh_request = RefreshTokenRequest(
        refresh_token=request.refresh_token,
    )

    response = service.refresh(refresh_request)

    return LoginUserResponseSchema.model_validate(response)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
def logout_user(
    request: LogoutRequestSchema,
    service: LogoutUserService = Depends(get_logout_user_service),
) -> dict[str, str]:

    service.logout(request.refresh_token)

    return {"message": "Logged out successfully."}
