from exreview.domain.enums.error_message import ErrorMessage


class UserAlreadyExistsError(Exception):

    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(ErrorMessage.USER_ALREADY_EXISTS)