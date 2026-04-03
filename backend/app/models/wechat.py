from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.database import Base

class WechatApp(Base):
    __tablename__ = "wechat_apps"

    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(String(50), unique=True, nullable=False)  # 微信应用ID
    app_secret = Column(String(100), nullable=False)  # 微信应用密钥
    app_type = Column(String(20), nullable=False)  # mini_program/official_account
    name = Column(String(100), nullable=False)  # 应用名称
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WechatUser(Base):
    __tablename__ = "wechat_users"

    id = Column(Integer, primary_key=True, index=True)
    union_id = Column(String(100))  # 微信union_id
    open_id = Column(String(100), unique=True, nullable=False)  # 微信open_id
    app_id = Column(String(50), nullable=False)  # 关联的微信应用
    nickname = Column(String(200))  # 昵称
    avatar_url = Column(Text)  # 头像
    gender = Column(Integer)  # 性别 0:未知 1:男 2:女
    city = Column(String(100))  # 城市
    province = Column(String(100))  # 省份
    country = Column(String(100))  # 国家
    language = Column(String(20))  # 语言
    phone_number = Column(String(20))  # 手机号
    invite_code = Column(String(50))  # 邀请码
    invited_by_wechat_open_id = Column(String(100))  # 邀请人微信open_id
    user_id = Column(Integer, ForeignKey("users.id"))  # 关联系统用户
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WechatInviteCode(Base):
    __tablename__ = "wechat_invite_codes"

    id = Column(Integer, primary_key=True, index=True)
    wechat_user_open_id = Column(String(100), nullable=False)  # 生成邀请码的微信用户
    invite_code = Column(String(50), unique=True, nullable=False)  # 邀请码
    qr_code_url = Column(Text)  # 邀请码二维码URL
    scene_param = Column(String(200))  # 场景参数
    channel_id = Column(Integer, ForeignKey("channels.id"))  # 关联渠道
    usage_count = Column(Integer, default=0)  # 使用次数
    max_usage = Column(Integer, default=0)  # 最大使用次数（0为无限制）
    expires_at = Column(DateTime)  # 过期时间
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WechatInviteRecord(Base):
    __tablename__ = "wechat_invite_records"

    id = Column(Integer, primary_key=True, index=True)
    inviter_open_id = Column(String(100), nullable=False)  # 邀请人微信open_id
    invitee_open_id = Column(String(100), nullable=False)  # 被邀请人微信open_id
    invite_code = Column(String(50), nullable=False)  # 邀请码
    invite_time = Column(DateTime, default=datetime.utcnow)  # 邀请时间
    register_time = Column(DateTime)  # 注册时间
    channel_id = Column(Integer, ForeignKey("channels.id"))  # 邀请渠道
    status = Column(String(20), default='pending')  # pending, registered, activated
    created_at = Column(DateTime, default=datetime.utcnow)

class WechatTemplateConfig(Base):
    __tablename__ = "wechat_template_configs"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(String(100), nullable=False)  # 模板ID
    template_name = Column(String(100), nullable=False)  # 模板名称
    app_id = Column(String(50), nullable=False)  # 微信应用ID
    template_content = Column(Text)  # 模板内容
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class WechatShareConfig(Base):
    __tablename__ = "wechat_share_configs"

    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(String(50), nullable=False)  # 微信应用ID
    share_title = Column(String(200))  # 分享标题
    share_description = Column(Text)  # 分享描述
    share_image_url = Column(Text)  # 分享图片
    redirect_url = Column(Text)  # 跳转链接
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
