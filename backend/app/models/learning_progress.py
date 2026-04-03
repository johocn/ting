from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class UserLearningSession(Base):
    """用户学习会话表"""
    __tablename__ = "user_learning_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # 实际应用中应关联用户表
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    session_id = Column(String(255), unique=True, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    watched_duration = Column(Integer, default=0)  # 已观看时长（秒）
    total_duration = Column(Integer)  # 总时长（秒）
    status = Column(String(50), default="in_progress")  # in_progress, completed, paused
    progress_percentage = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LearningAchievement(Base):
    """学习成就表"""
    __tablename__ = "learning_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    achievement_type = Column(String(100), nullable=False)  # completed, milestone, etc.
    achievement_name = Column(String(200), nullable=False)
    achievement_description = Column(Text)
    points_earned = Column(Integer, default=0)
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    is_rewarded = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)