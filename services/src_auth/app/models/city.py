from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship
from libs.shared.utils.base_model import BaseModel


class City(BaseModel):
    __tablename__ = "cities"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    postal_code = Column(String(30))

    stores = relationship("Store", back_populates="city")
