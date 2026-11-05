
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt

from exreview.infrastructure.config.settings import Settings


class PyJWTTokenProvider:

    def __init__(self, settings: Settings) -> None:
        if not settings.jwt_secret_key:
            raise RuntimeError("JWT_SECRET_KEY is not configured.")

        if len(settings.jwt_secret_key.encode("utf-8")) < 32:
            raise RuntimeError("JWT_SECRET_KEY must be at least 32 bytes.")

        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm

        self.access_expiry = timedelta(
            minutes=settings.access_token_expire_minutes
        )

        self.refresh_expiry = timedelta(
            days=settings.refresh_token_expire_days
        )

    def create_access_token(self, subject: str) -> str:
        return self._create_token(subject, "access", self.access_expiry)

    def create_refresh_token(self, subject: str) -> str:
        return self._create_token(subject, "refresh", self.refresh_expiry)

    def _create_token(
        self,
        subject: str,
        token_type: str,
        expiry: timedelta,
    ) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": subject,
            "type": token_type,
            "iat": now,
            "exp": now + expiry,
            "jti": str(uuid4()),
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def _get_token_subject(
        self,
        token: str,
        expected_type: str,
    ) -> str | None:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={
                    "require": ["sub", "exp", "iat", "jti", "type"]
                },
            )

            if payload.get("type") != expected_type:
                return None

            subject = payload.get("sub")

            return subject if isinstance(subject, str) else None

        except jwt.InvalidTokenError:
            return None

    def get_access_token_subject(self, token: str) -> str | None:
        return self._get_token_subject(token, "access")

    def get_refresh_token_subject(self, token: str) -> str | None:
        return self._get_token_subject(token, "refresh")
