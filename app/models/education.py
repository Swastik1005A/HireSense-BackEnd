from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)

    candidate_id = Column(Integer, ForeignKey("candidates.id"))

    degree = Column(String(255), nullable=True)
    field_of_study = Column(String(255), nullable=True)
    institution = Column(String(255), nullable=True)
    graduation_year = Column(Integer, nullable=True)