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
from .learning_progress import UserLearningSession, LearningAchievement
from .sign_notifications import SignRecord, Notification, extend_user_model

# 扩展用户模型
extend_user_model(User)
