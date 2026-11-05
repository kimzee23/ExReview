import hashlib

from exreview.application.ports.token_hasher import TokenHasher


class SHA256TokenHasher(TokenHasher):

    def hash(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()