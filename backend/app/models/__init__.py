from .users import User
from .contents import Content, Question, ContentQuizConfig
from .points import UserPointAccount, PointTransaction, PointExpirationRule
from .channels import (
    ChannelType, Channel, ChannelUserRelation, ChannelStatistics,
    ChannelPermission, ChannelPointConfig, ChannelHierarchy, ChannelInvitationRecord
)
from .mall import (
    ProductCategory, Product, ExchangeRecord, Store,
    VerificationRecord, StoreEmployee, VerificationPermission
)
from .wechat import (
    WechatApp, WechatUser, WechatInviteCode, WechatInviteRecord,
    WechatTemplateConfig, WechatShareConfig
)

# 导入Base以确保所有模型都被注册
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
