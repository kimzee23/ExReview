from exreview.domain.enums.error_message import ErrorMessage


class InvalidCredentialsError(Exception):

    def __init__(self) -> None:
        super().__init__(ErrorMessage.INVALID_CREDENTIALS.value)