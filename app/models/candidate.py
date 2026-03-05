from sqlalchemy import Column , Integer , String , Text , JSON
from app.database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer , primary_key=True , index=True)
    name = Column(String(255) , nullable=False)
    email = Column(String(255) , unique=True , nullable=False , index=True)

    resume_text = Column(Text , nullable=False)
    skills = Column(JSON , nullable=True)
    experience_years = Column(Integer , nullable=True)
    experience_level = Column(String(50) , nullable=True)