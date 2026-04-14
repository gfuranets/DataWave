from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

user = "root"
password = "root"
host = "127.0.0.1"
port = 3306
database = "DataWave"
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
                bind = engine,
                autocommit = False,
                autoflush = False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
