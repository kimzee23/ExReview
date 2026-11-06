from fastapi import FastAPI
from exreview.presentation.routers.user_router import router as user_router
from exreview.domain.exceptions.invalid_password import InvalidPasswordError
from exreview.domain.exceptions.user_already_exists import UserAlreadyExistsError
from exreview.presentation.exception_handlers import (
    handle_invalid_password,
    handle_invalid_credentials,
    handle_request_validation_error,
    handle_user_already_exists,
)
from exreview.domain.exceptions.invalid_credentials import (
    InvalidCredentialsError,
)
from fastapi.exceptions import RequestValidationError

from exreview.domain.exceptions.invalid_access_token import (
    InvalidAccessTokenError,
)

from exreview.presentation.exception_handlers import (
    handle_invalid_access_token,
)
from exreview.domain.exceptions.invalid_refresh_token import ( InvalidRefreshTokenError,)

from fastapi.responses import JSONResponse
from fastapi import status
from exreview.presentation.routers.experience_router import router as experience_router


app = FastAPI(
    title="Ex Review",
    description="A platform for sharing relation experiences",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {"message": "Welcome to ExReview API",
            "status": "Application is running"}

app.include_router(user_router)
app.include_router(experience_router)

app.add_exception_handler(
    UserAlreadyExistsError,
    handle_user_already_exists,
)

app.add_exception_handler(
    InvalidPasswordError,
    handle_invalid_password,
)

app.add_exception_handler(
    RequestValidationError,
    handle_request_validation_error,
)

app.add_exception_handler(
    InvalidCredentialsError,
    handle_invalid_credentials,
)
app.add_exception_handler(
    InvalidAccessTokenError,
    handle_invalid_access_token,
)

@app.exception_handler(InvalidRefreshTokenError)
async def invalid_refresh_token_handler(request, exception):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exception)},
    )