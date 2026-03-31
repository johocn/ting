from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    url = Column(String(500), nullable=False)
    duration = Column(Integer, default=0)  # 时长（秒）
    category = Column(String(50))
    reward_points_per_minute = Column(Integer, default=5)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"))
    question_text = Column(Text, nullable=False)
    options = Column(JSON)  # 题目选项
    correct_answer = Column(String(10))  # 正确答案
    individual_points = Column(Integer, default=20)
    question_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class ContentQuizConfig(Base):
    __tablename__ = "content_quiz_configs"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), unique=True)
    total_questions = Column(Integer, default=10)
    required_correct = Column(Integer, default=8)
    pass_percentage = Column(Integer, default=80)  # 及格百分比
    quiz_points = Column(Integer, default=100)  # 答题奖励积分
    time_limit = Column(Integer)  # 答题时间限制（秒）
    allow_retry = Column(Boolean, default=False)
    retry_limit = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
