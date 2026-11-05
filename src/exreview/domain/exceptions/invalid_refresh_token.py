
from exreview.domain.enums.error_message import ErrorMessage


class InvalidRefreshTokenError(Exception):

    def __init__(self) -> None:
        super().__init__(ErrorMessage.INVALID_REFRESH_TOKEN.value)
