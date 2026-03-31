from pydantic import BaseModel
from typing import Optional, Dict, Any

class ChannelTypeBase(BaseModel):
    name: str
    description: Optional[str] = ""
    is_active: Optional[bool] = True

class ChannelTypeCreate(ChannelTypeBase):
    pass

class ChannelTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ChannelBase(BaseModel):
    name: str
    type_id: int
    parent_channel_id: Optional[int] = None
    commission_rate: Optional[float] = 0.0
    settings: Optional[Dict[str, Any]] = {}

class ChannelCreate(ChannelBase):
    pass

class ChannelUpdate(BaseModel):
    name: Optional[str] = None
    type_id: Optional[int] = None
    parent_channel_id: Optional[int] = None
    commission_rate: Optional[float] = None
    settings: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class ChannelUserRelationBase(BaseModel):
    channel_id: int
    user_id: int
    level: Optional[int] = 1
    is_active: Optional[bool] = True

class ChannelUserRelationCreate(ChannelUserRelationBase):
    pass

class ChannelUserRelationUpdate(BaseModel):
    level: Optional[int] = None
    is_active: Optional[bool] = None

class ChannelStatisticsBase(BaseModel):
    channel_id: int
    registered_users: Optional[int] = 0
    active_users: Optional[int] = 0
    earned_points: Optional[int] = 0
    spent_points: Optional[int] = 0
    exchange_count: Optional[int] = 0
    verification_count: Optional[int] = 0

class ChannelStatisticsCreate(ChannelStatisticsBase):
    pass

class ChannelStatisticsUpdate(BaseModel):
    registered_users: Optional[int] = None
    active_users: Optional[int] = None
    earned_points: Optional[int] = None
    spent_points: Optional[int] = None
    exchange_count: Optional[int] = None
    verification_count: Optional[int] = None
