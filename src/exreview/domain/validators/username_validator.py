import re


USERNAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]{2,29}$")


def normalize_username(username: str) -> str:
    return username.strip().lower()


def validate_username(username: str) -> None:
    normalized = normalize_username(username)

    if not USERNAME_PATTERN.fullmatch(normalized):
        raise ValueError(
            "Username must be 3–30 characters, start with a letter, "
            "and contain only letters, numbers, and underscores."
        )