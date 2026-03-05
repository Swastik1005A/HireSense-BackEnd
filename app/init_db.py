from app.database import engine, Base

# Import ALL models so SQLAlchemy registers them
from app.models.candidate import Candidate
from app.models.education import Education
from app.models.job_description import JobDescription
from app.models.score import Score


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Tables created successfully.")