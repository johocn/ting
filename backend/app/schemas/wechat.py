from pydantic import BaseModel
from typing import Optional, Dict, Any

class WechatLoginRequest(BaseModel):
    code: str
    encrypted_data: str
    iv: str
    raw_data: str
    signature: str
    user_info: Dict[str, Any]  # 微信用户信息
    invite_code: Optional[str] = ""
    channel_code: Optional[str] = ""

class WechatRegisterRequest(BaseModel):
    code: str
    encrypted_data: str
    iv: str
    raw_data: str
    signature: str
    user_info: Dict[str, Any]
    invite_code: Optional[str] = ""
    phone: Optional[str] = ""

class PhoneBindRequest(BaseModel):
    phone: str
    captcha: str

class WechatAppBase(BaseModel):
    app_id: str
    app_secret: str
    app_type: str  # mini_program/official_account
    name: str
    description: Optional[str] = ""
    is_active: Optional[bool] = True

class WechatAppCreate(WechatAppBase):
    pass

class WechatAppUpdate(BaseModel):
    app_id: Optional[str] = None
    app_secret: Optional[str] = None
    app_type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class WechatUserUpdate(BaseModel):
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[int] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    language: Optional[str] = None
    phone_number: Optional[str] = None
    invite_code: Optional[str] = None
    invited_by_wechat_open_id: Optional[str] = None
