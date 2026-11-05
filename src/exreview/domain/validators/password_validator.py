from exreview.domain.enums.error_message import ErrorMessage
from exreview.domain.exceptions.invalid_password import InvalidPasswordError

def validate_password(password: str) -> None:
    requirements = {
    ErrorMessage.PASSWORD_TOO_SHORT: len(password) >= 8,
    ErrorMessage.PASSWORD_UPPERCASE_REQUIRED: any(char.isupper() for char in password),
    ErrorMessage.PASSWORD_LOWERCASE_REQUIRED: any(char.islower() for char in password),
    ErrorMessage.PASSWORD_NUMBER_REQUIRED: any(char.isdigit() for char in password),
    ErrorMessage.PASSWORD_SPECIAL_CHARACTER_REQUIRED: any(
            not char.isalnum() and not char.isspace()
            for char in password
        ),
    }
    failed_requirements = [
        requirement
        for requirement, satisfied in requirements.items()
        if not satisfied
    ]
    if failed_requirements:
        raise InvalidPasswordError(failed_requirements)


