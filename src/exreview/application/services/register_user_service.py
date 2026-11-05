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
from exreview.domain.validators.password_validator import validate_password


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

        # Check whether the email is already registered.
        existing_user = self.user_repository.find_by_email(email)

        if existing_user is not None:
            raise UserAlreadyExistsError(email)

        # Validate the password against our domain rules.
        validate_password(request.password)

        # Hash the password before storing it.
        password_hash = self.password_hasher.hash(request.password)

        # Create the domain entity.
        user = User(
            id=uuid4(),
            email=email,
            password_hash=password_hash,
            display_name=request.display_name.strip(),
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )

        # Persist the user.
        saved_user = self.user_repository.save(user)

        # Return the registration response.
        return RegisterUserResponse(
            id=saved_user.id,
            email=saved_user.email,
            display_name=saved_user.display_name,
            is_active=saved_user.is_active,
            created_at=saved_user.created_at,
        )