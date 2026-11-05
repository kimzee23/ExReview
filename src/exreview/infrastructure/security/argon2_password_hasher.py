from pwdlib import PasswordHash as PwdlibPasswordHash

from exreview.application.ports.password_hasher import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):

    def __init__(self) -> None:
        self._password_hash = PwdlibPasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self._password_hash.hash(password)

    def verify(
        self,
        password: str,
        hashed_password: str
    ) -> bool:
        return self._password_hash.verify(password, hashed_password)