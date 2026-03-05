from sqlalchemy import Column , Integer , Float , ForeignKey, String
from app.database import Base

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer , primary_key=True , index=True)

    candidate_id = Column(Integer , ForeignKey("candidates.id"))
    job_id = Column(Integer , ForeignKey("job_descriptions.id"))

    semantic_score = Column(Float)
    skill_score = Column(Float)
    experience_score = Column(Float)
    

    final_score = Column(Float)
    bias_flag = Column(String)