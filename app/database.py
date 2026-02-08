from .config import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus


settings = Settings()
engine = create_engine(
    f"postgresql://{settings.DB_USER}:{quote_plus(settings.DB_PASSWORD)}@{settings.DB_SERVER}:{settings.DB_PORT}/{settings.DB_NAME}?sslmode=require"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





