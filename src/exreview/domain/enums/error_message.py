from enum import StrEnum


class ErrorMessage(StrEnum):

    # User errors
    USER_ALREADY_EXISTS = "An account with this email already exists."

    # Password validation errors
    PASSWORD_TOO_SHORT = "at least 8 characters"
    PASSWORD_UPPERCASE_REQUIRED = "at least one uppercase letter"
    PASSWORD_LOWERCASE_REQUIRED = "at least one lowercase letter"
    PASSWORD_NUMBER_REQUIRED = "at least one number"
    PASSWORD_SPECIAL_CHARACTER_REQUIRED = "at least one special character"

    INVALID_PASSWORD = "Password must contain: {requirements}."

    # Request validation errors
    REQUEST_VALIDATION_FAILED = "Request validation failed."
    FIELD_REQUIRED = "This field is required."
    INVALID_EMAIL = "Enter a valid email address."
    FIELD_TOO_SHORT = "Value is too short."
    FIELD_TOO_LONG = "Value is too long."
    INVALID_FIELD = "Invalid value."
    INVALID_CREDENTIALS = "Email or password is incorrect."
    INVALID_ACCESS_TOKEN = "Authentication credentials are invalid or expired."

    INVALID_REFRESH_TOKEN = "Refresh token is invalid, expired, or revoked."