class UsernameAlreadyExistsError(Exception):

    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(
            f"The username '@{username}' is already taken."
        )