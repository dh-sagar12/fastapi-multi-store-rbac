from sqlalchemy import BigInteger, Column, ForeignKey, Text
from libs.shared.utils.base_model import BaseModel
from sqlalchemy.orm import relationship


class TokenBlacklist(BaseModel):
    """We only stores blacklisted access tokens in this table"""

    __tablename__ = "token_blacklists"

    id = Column(BigInteger, primary_key=True)
    token = Column(Text, unique=True, nullable=False, index=True)
    user_id = Column(
        BigInteger, ForeignKey("users.id"), nullable=False, index=True
    )

    user = relationship("User", back_populates="token_blacklists")
