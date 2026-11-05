from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette import status

from exreview.domain.enums.error_message import ErrorMessage
from exreview.domain.exceptions.invalid_password import InvalidPasswordError
from exreview.domain.exceptions.user_already_exists import (
    UserAlreadyExistsError,
)
from exreview.domain.exceptions.invalid_access_token import (
    InvalidAccessTokenError,
)



async def handle_user_already_exists(
    request: Request,
    exception: UserAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": ErrorMessage.USER_ALREADY_EXISTS.value
        },
    )


async def handle_invalid_password(
    request: Request,
    exception: InvalidPasswordError,
) -> JSONResponse:
    return JSONResponse(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": str(exception)
        },
    )

from fastapi.exceptions import RequestValidationError


async def handle_request_validation_error(
    request: Request,
    exception: RequestValidationError,
) -> JSONResponse:

    validation_errors = []

    for error in exception.errors():
        location = error.get("loc", ())
        field_parts = [
            str(part)
            for part in location
            if part not in {"body", "query", "path", "header", "cookie"}
        ]

        field = ".".join(field_parts) or "request"
        error_type = error.get("type")

        if error_type == "missing":
            message = ErrorMessage.FIELD_REQUIRED.value

        elif field == "email":
            message = ErrorMessage.INVALID_EMAIL.value

        elif error_type == "string_too_short":
            message = ErrorMessage.FIELD_TOO_SHORT.value

        elif error_type == "string_too_long":
            message = ErrorMessage.FIELD_TOO_LONG.value

        else:
            message = ErrorMessage.INVALID_FIELD.value

        validation_errors.append({
            "field": field,
            "message": message,
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": ErrorMessage.REQUEST_VALIDATION_FAILED.value,
            "errors": validation_errors,
        },
    )

from exreview.domain.exceptions.invalid_credentials import (
    InvalidCredentialsError,
)


async def handle_invalid_credentials(
    request: Request,
    exception: InvalidCredentialsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": ErrorMessage.INVALID_CREDENTIALS.value
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

async def handle_invalid_access_token(
    request: Request,
    exception: InvalidAccessTokenError,
) -> JSONResponse:

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": ErrorMessage.INVALID_ACCESS_TOKEN.value
        },
        headers={"WWW-Authenticate": "Bearer"},
    )