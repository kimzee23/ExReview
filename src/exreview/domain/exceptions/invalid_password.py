from exreview.domain.enums.error_message import ErrorMessage


class InvalidPasswordError(ValueError):

    def __init__(self, requirements: list[str]) -> None:
        self.requirements = requirements

        message = ErrorMessage.INVALID_PASSWORD.value.format(
            requirements=", ".join(requirements)
        )

        super().__init__(message)