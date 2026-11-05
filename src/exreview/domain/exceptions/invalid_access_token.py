from exreview.domain.enums.error_message import ErrorMessage


class InvalidAccessTokenError(Exception):

    def __init__(self) -> None:
        super().__init__(ErrorMessage.INVALID_ACCESS_TOKEN.value)