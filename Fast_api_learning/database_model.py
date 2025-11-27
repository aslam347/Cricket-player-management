from sqlalchemy import Column, Integer, String, Float
from db_connection import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    role = Column(String(50))
    matches = Column(Integer)
    runs = Column(Integer)
    wickets = Column(Integer)
    strike_rate = Column(Float)
    economy_rate = Column(Float)
    best_performance = Column(String(100))
