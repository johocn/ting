from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.database import Base

class UserPointAccount(Base):
    __tablename__ = "user_point_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    total_points = Column(Integer, default=0)  # 总积分
    available_points = Column(Integer, default=0)  # 可用积分
    frozen_points = Column(Integer, default=0)  # 冻结积分
    expired_points = Column(Integer, default=0)  # 已过期积分
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PointTransaction(Base):
    __tablename__ = "point_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_type = Column(String(50))  # earn/spend/freeze/thaw
    operation_type = Column(String(50))  # watch_video, answer_quiz, purchase, exchange
    points_change = Column(Integer)  # 积分变化量
    balance_before = Column(Integer)  # 变化前余额
    balance_after = Column(Integer)  # 变化后余额
    related_id = Column(Integer)  # 相关记录ID
    description = Column(Text)  # 描述
    expiration_date = Column(DateTime)  # 过期日期
    status = Column(String(20), default='active')  # active, expired, canceled
    created_at = Column(DateTime, default=datetime.utcnow)

class PointExpirationRule(Base):
    __tablename__ = "point_expiration_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String(100), nullable=False)
    validity_period_days = Column(Integer, default=365)  # 有效期天数
    apply_to_new = Column(Boolean, default=True)  # 是否应用于新积分
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
