from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config
database_url = config('database_url')
SQLAlCHEMY_DATABASE_URL = database_url
engine = create_engine(
    SQLAlCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()