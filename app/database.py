from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import settings


try:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}\
                                @{settings.database_hostname}:{settings.database_port}/{settings.database_name}?sslmode=require"
    print(f"Connecting to database at: {settings.database_hostname}:{settings.database_port} with user {settings.database_username}")
    
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=True,
        autocommit=False
    )

    Base = declarative_base()

except Exception as e:
    print(f"Error while connecting to the database: {str(e)}")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()