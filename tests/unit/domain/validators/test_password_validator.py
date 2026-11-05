import pytest

from exreview.domain.validators.password_validator import validate_password


def test_valid_password():
    validate_password("Password1@")


@pytest.mark.parametrize(
    "password",
    [
        "Pass1@",       # Less than 8 characters
        "password1@",   # Missing uppercase
        "PASSWORD1@",   # Missing lowercase
        "Password@",    # Missing number
        "Password1",    # Missing special character
    ],
)
def test_invalid_password(password):
    with pytest.raises(ValueError):
        validate_password(password)