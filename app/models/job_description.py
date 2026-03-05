from sqlalchemy import Column , Integer , Text
from app.database import Base
class JobDescription(Base):
    __tablename__ = "job_descriptions"
    id = Column(Integer , primary_key=True , index=True)
    description_text = Column(Text , nullable=False)