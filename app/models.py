from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    timestamp = Column(DateTime)
