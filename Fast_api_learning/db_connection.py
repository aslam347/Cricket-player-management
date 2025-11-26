from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "mysql+pymysql://root:Aslam%402001@localhost:3306/ipl_db"

engine = create_engine(db_url)
session  = sessionmaker(autoflush=False,autocommit = False, bind=engine)