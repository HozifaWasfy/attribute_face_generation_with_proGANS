from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/progan_database"

engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

