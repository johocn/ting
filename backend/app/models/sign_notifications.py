from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class SignRecord(Base):
    """
    签到记录模型
    """
    __tablename__ = "sign_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sign_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 签到日期
    points_awarded = Column(Integer, default=0)  # 获得积分
    continuous_days = Column(Integer, default=1)  # 连续签到天数
    is_reward_claimed = Column(Boolean, default=False)  # 是否已领取奖励
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联用户
    user = relationship("User", back_populates="sign_records")


class Notification(Base):
    """
    通知消息模型
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 接收用户
    title = Column(String(200), nullable=False)  # 通知标题
    content = Column(Text, nullable=False)  # 通知内容
    notification_type = Column(String(50), default="system")  # 通知类型: system, points, promotion
    related_id = Column(String(100), nullable=True)  # 相关ID（如订单ID、学习会话ID等）
    is_read = Column(Boolean, default=False)  # 是否已读
    priority = Column(Integer, default=1)  # 优先级: 1-low, 2-medium, 3-high
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
    read_at = Column(DateTime(timezone=True), nullable=True)  # 阅读时间

    # 关联用户
    user = relationship("User", back_populates="notifications")


# 在User模型中添加关联
def extend_user_model(User):
    """扩展User模型，添加签到和通知关联"""
    User.sign_records = relationship("SignRecord", back_populates="user", order_by=SignRecord.sign_date.desc())
    User.notifications = relationship("Notification", back_populates="user", order_by=Notification.created_at.desc())
