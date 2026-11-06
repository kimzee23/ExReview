class UsernameAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__("Username is already taken.")