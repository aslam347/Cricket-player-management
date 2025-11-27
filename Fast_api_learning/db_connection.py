# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# db_url = "mysql+pymysql://root:Aslam%402001@localhost:3306/ipl_db"
#
# engine = create_engine(db_url)
# session  = sessionmaker(autoflush=False,autocommit = False, bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:Aslam%402001@localhost/ipl_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal
Base = declarative_base()
