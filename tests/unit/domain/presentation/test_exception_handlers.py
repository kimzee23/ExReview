import asyncio
import json
from unittest.mock import Mock

from fastapi import Request
from fastapi.exceptions import RequestValidationError

from exreview.domain.enums.error_message import ErrorMessage
from exreview.presentation.exception_handlers import (
    handle_request_validation_error,
)


def test_request_validation_handler():
    exception = RequestValidationError([
        {
            "type": "value_error",
            "loc": ("body", "email"),
            "msg": "Invalid email",
            "input": "invalid-email",
        },
        {
            "type": "missing",
            "loc": ("body", "display_name"),
            "msg": "Field required",
            "input": None,
        },
    ])

    response = asyncio.run(
        handle_request_validation_error(
            Mock(spec=Request),
            exception,
        )
    )

    body = json.loads(response.body)

    assert response.status_code == 422
    assert body["detail"] == ErrorMessage.REQUEST_VALIDATION_FAILED.value

    assert body["errors"] == [
        {
            "field": "email",
            "message": ErrorMessage.INVALID_EMAIL.value,
        },
        {
            "field": "display_name",
            "message": ErrorMessage.FIELD_REQUIRED.value,
        },
    ]