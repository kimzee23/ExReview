from datetime import datetime, timezone
from uuid import uuid4

from exreview.application.dto.requests.register_user_request import (
    RegisterUserRequest,
)
from exreview.application.dto.responses.register_user_response import (
    RegisterUserResponse,
)
from exreview.application.ports.password_hasher import PasswordHasher
from exreview.application.ports.user_repository import UserRepository
from exreview.domain.entities.user import User
from exreview.domain.exceptions.user_already_exists import (
    UserAlreadyExistsError,
)
from exreview.domain.exceptions.username_already_exists import (
    UsernameAlreadyExistsError,
)
from exreview.domain.validators.password_validator import validate_password
from exreview.domain.validators.username_validator import normalize_username


class RegisterUserService:

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def register(
        self,
        request: RegisterUserRequest,
    ) -> RegisterUserResponse:

        email = request.email.strip().lower()
        username = normalize_username(request.username)

        existing_user = self.user_repository.find_by_email(email)

        if existing_user is not None:
            raise UserAlreadyExistsError(email)

        existing_username = self.user_repository.find_by_username(username)

        if existing_username is not None:
            raise UsernameAlreadyExistsError(username)

        validate_password(request.password)

        password_hash = self.password_hasher.hash(request.password)

        user = User(
            id=uuid4(),
            email=email,
            username=username,
            password_hash=password_hash,
            display_name=request.display_name.strip(),
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )

        saved_user = self.user_repository.save(user)

        return RegisterUserResponse(
            id=saved_user.id,
            email=saved_user.email,
            username=saved_user.username,
            display_name=saved_user.display_name,
            is_active=saved_user.is_active,
            created_at=saved_user.created_at,
        )