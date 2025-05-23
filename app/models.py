from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)

    # 10个评分维度
    score1 = Column(Integer, nullable=True)
    score2 = Column(Integer, nullable=True)
    score3 = Column(Integer, nullable=True)
    score4 = Column(Integer, nullable=True)
    score5 = Column(Integer, nullable=True)
    score6 = Column(Integer, nullable=True)
    score7 = Column(Integer, nullable=True)
    score8 = Column(Integer, nullable=True)
    score9 = Column(Integer, nullable=True)
    score10 = Column(Integer, nullable=True)
