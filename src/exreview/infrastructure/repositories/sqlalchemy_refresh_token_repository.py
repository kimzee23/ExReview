
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from exreview.application.ports.refresh_token_repository import (
    RefreshTokenRepository,
)
from exreview.domain.entities.refresh_token import RefreshToken
from exreview.infrastructure.models.refresh_token_model import (
    RefreshTokenModel,
)


class SQLAlchemyRefreshTokenRepository(RefreshTokenRepository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, refresh_token: RefreshToken) -> None:
        model = RefreshTokenModel(
            user_id=refresh_token.user_id,
            token_hash=refresh_token.token_hash,
            expires_at=refresh_token.expires_at,
            revoked_at=refresh_token.revoked_at,
        )

        self.session.add(model)
        self.session.commit()

    def find_by_hash(self, token_hash: str) -> RefreshToken | None:
        model = self.session.scalar(
            select(RefreshTokenModel).where(
                RefreshTokenModel.token_hash == token_hash
            )
        )

        if model is None:
            return None

        return RefreshToken(
            id=model.id,
            user_id=model.user_id,
            token_hash=model.token_hash,
            expires_at=model.expires_at,
            revoked_at=model.revoked_at,
        )

    def rotate(
        self,
        old_token_hash: str,
        new_refresh_token: RefreshToken
    ) -> bool:
        now = datetime.now(timezone.utc)

        try:
            result = self.session.execute(
                update(RefreshTokenModel)
                .where(
                    RefreshTokenModel.token_hash == old_token_hash,
                    RefreshTokenModel.revoked_at.is_(None),
                    RefreshTokenModel.expires_at > now,
                )
                .values(revoked_at=now)
            )

            if result.rowcount != 1:
                self.session.rollback()
                return False

            self.session.add(
                RefreshTokenModel(
                    user_id=new_refresh_token.user_id,
                    token_hash=new_refresh_token.token_hash,
                    expires_at=new_refresh_token.expires_at,
                    revoked_at=None,
                )
            )

            self.session.commit()
            return True

        except Exception:
            self.session.rollback()
            raise

    def revoke(self, token_hash: str) -> bool:
        now = datetime.now(timezone.utc)

        result = self.session.execute(
            update(RefreshTokenModel)
            .where(
                RefreshTokenModel.token_hash == token_hash,
                RefreshTokenModel.revoked_at.is_(None),
                RefreshTokenModel.expires_at > now,
            )
            .values(revoked_at=now)
        )

        self.session.commit()
        return result.rowcount == 1
