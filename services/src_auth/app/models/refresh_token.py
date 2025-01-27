from sqlalchemy import BigInteger, Column, String, Text, ForeignKey
from libs.shared.utils.base_model import BaseModel
from sqlalchemy.orm import relationship


class RefreshToken(BaseModel):
    """Refresh token model definition."""

    __tablename__ = "refresh_tokens"

    id = Column(BigInteger, primary_key=True, index=True)
    token = Column(Text, unique=True, nullable=False, index=True)
    user_id = Column(
        BigInteger, ForeignKey("users.id"), nullable=False, index=True
    )
    access_token_jti = Column(
        String(255), nullable=False, unique=True, index=True
    )

    user = relationship("User", back_populates="refresh_tokens")
