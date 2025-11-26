from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column

Base = declarative_base()

class Ipl(Base):
   __tablename__ = "ipl"

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String(100))   # ✅ added length
   age = Column(String(10))     # ✅ added length
   score = Column(Integer)
