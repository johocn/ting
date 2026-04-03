from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, UniqueConstraint
from datetime import datetime
from app.database import Base

class ChannelType(Base):
    __tablename__ = "channel_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False)  # 邀请码
    type_id = Column(Integer, ForeignKey("channel_types.id"))
    creator_user_id = Column(Integer, ForeignKey("users.id"))  # 创建者
    parent_channel_id = Column(Integer, ForeignKey("channels.id"))  # 上级渠道
    level = Column(Integer, default=1)  # 渠道层级
    commission_rate = Column(Integer, default=0)  # 佣金比例
    invite_link = Column(Text)  # 邀请链接
    qr_code_url = Column(Text)  # 二维码链接
    settings = Column(JSON)  # 渠道设置
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChannelUserRelation(Base):
    __tablename__ = "channel_user_relations"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    joined_at = Column(DateTime, default=datetime.utcnow)
    invited_by = Column(Integer, ForeignKey("users.id"))  # 邀请人
    level = Column(Integer, default=1)  # 用户在渠道中的层级
    is_active = Column(Boolean, default=True)
    __table_args__ = (UniqueConstraint('channel_id', 'user_id'),)

class ChannelStatistics(Base):
    __tablename__ = "channel_statistics"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    date = Column(DateTime, default=datetime.utcnow)
    registered_users = Column(Integer, default=0)  # 注册用户数
    active_users = Column(Integer, default=0)  # 活跃用户数
    earned_points = Column(Integer, default=0)  # 获得积分总数
    spent_points = Column(Integer, default=0)  # 消耗积分总数
    exchange_count = Column(Integer, default=0)  # 兑换次数
    verification_count = Column(Integer, default=0)  # 核销次数
    updated_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('channel_id', 'date'),)

class ChannelPermission(Base):
    __tablename__ = "channel_permissions"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    permission_code = Column(String(100), nullable=False)  # 权限代码
    permission_name = Column(String(200), nullable=False)  # 权限名称
    is_allowed = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChannelPointConfig(Base):
    __tablename__ = "channel_point_configs"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    config_type = Column(String(50), nullable=False)  # 配置类型：watch_video, answer_quiz等
    multiplier = Column(Integer, default=100)  # 积分倍数（百分比）
    fixed_bonus = Column(Integer, default=0)  # 固定奖励
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChannelHierarchy(Base):
    __tablename__ = "channel_hierarchy"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    parent_id = Column(Integer, ForeignKey("channels.id"))
    level = Column(Integer, nullable=False)  # 层级编号
    path = Column(String(500))  # 层级路径（如：1/5/12）
    depth = Column(Integer, nullable=False)  # 深度
    created_at = Column(DateTime, default=datetime.utcnow)

class ChannelInvitationRecord(Base):
    __tablename__ = "channel_invitation_records"

    id = Column(Integer, primary_key=True, index=True)
    inviter_user_id = Column(Integer, ForeignKey("users.id"))  # 邀请人
    invitee_user_id = Column(Integer, ForeignKey("users.id"))  # 被邀请人
    channel_id = Column(Integer, ForeignKey("channels.id"))  # 邀请渠道
    invitation_code = Column(String(50))  # 邀请码
    invite_time = Column(DateTime, default=datetime.utcnow)
    registration_time = Column(DateTime)  # 注册时间
    status = Column(String(20), default='pending')  # pending, registered, activated
    ip_address = Column(String(45))  # IP地址
    user_agent = Column(Text)  # User-Agent
