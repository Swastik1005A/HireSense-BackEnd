from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from app.config import settings

#Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    connect_args={"ssl": {"ssl-mode": "REQUIRED"}}
)

# Create session Factory
SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)

# Base class for ORM models
Base = declarative_base()

#Dependency to get DB session in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()