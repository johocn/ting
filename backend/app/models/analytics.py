from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Index
from sqlalchemy.sql import func
from app.database import Base


class UserBehavior(Base):
    """
    用户行为统计模型
    """
    __tablename__ = "user_behaviors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # 用户ID
    action_type = Column(String(50), nullable=False)  # 行为类型 (login, view_content, earn_points, exchange_item, etc.)
    action_target = Column(String(100), nullable=True)  # 行为目标 (content_id, product_id, etc.)
    action_value = Column(Float, nullable=True)  # 行为值 (积分变化量等)
    session_id = Column(String(100), nullable=True)  # 会话ID
    ip_address = Column(String(45), nullable=True)  # IP地址
    user_agent = Column(Text, nullable=True)  # 用户代理
    referrer = Column(Text, nullable=True)  # 来源页面
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间

    # 索引
    __table_args__ = (
        Index('idx_user_behavior_user_id', 'user_id'),
        Index('idx_user_behavior_action_type', 'action_type'),
        Index('idx_user_behavior_created_at', 'created_at'),
    )


class ConversionRate(Base):
    """
    转化率统计模型
    """
    __tablename__ = "conversion_rates"

    id = Column(Integer, primary_key=True, index=True)
    conversion_type = Column(String(50), nullable=False)  # 转化类型 (registration_to_first_learn, first_learn_to_exchange, etc.)
    funnel_step = Column(String(50), nullable=False)  # 漏斗步骤
    user_count = Column(Integer, default=0)  # 用户数量
    total_users = Column(Integer, default=0)  # 总用户数 (用于计算转化率)
    conversion_rate = Column(Float, default=0.0)  # 转化率
    period_start = Column(DateTime(timezone=True), nullable=False)  # 统计周期开始
    period_end = Column(DateTime(timezone=True), nullable=False)  # 统计周期结束
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间

    # 索引
    __table_args__ = (
        Index('idx_conversion_type', 'conversion_type'),
        Index('idx_conversion_period', 'period_start', 'period_end'),
    )


class UserEngagement(Base):
    """
    用户参与度统计模型
    """
    __tablename__ = "user_engagements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # 用户ID
    login_days = Column(Integer, default=0)  # 登录天数
    content_views = Column(Integer, default=0)  # 内容浏览次数
    videos_completed = Column(Integer, default=0)  # 完成视频数
    points_earned = Column(Integer, default=0)  # 获得积分
    items_exchanged = Column(Integer, default=0)  # 兑换商品数
    sign_ins = Column(Integer, default=0)  # 签到次数
    last_activity_at = Column(DateTime(timezone=True), server_default=func.now())  # 最后活动时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # 更新时间

    # 索引
    __table_args__ = (
        Index('idx_user_engagement_user_id', 'user_id'),
    )