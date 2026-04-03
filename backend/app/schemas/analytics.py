from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class UserBehaviorCreate(BaseModel):
    action_type: str
    action_target: Optional[str] = None
    action_value: Optional[float] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None

    class Config:
        from_attributes = True


class UserBehaviorResponse(BaseModel):
    id: int
    user_id: int
    action_type: str
    action_target: Optional[str] = None
    action_value: Optional[float] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversionRateResponse(BaseModel):
    id: int
    conversion_type: str
    funnel_step: str
    user_count: int
    total_users: int
    conversion_rate: float
    period_start: datetime
    period_end: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class UserEngagementResponse(BaseModel):
    id: int
    user_id: int
    login_days: int
    content_views: int
    videos_completed: int
    points_earned: int
    items_exchanged: int
    sign_ins: int
    last_activity_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalyticsSummaryResponse(BaseModel):
    user_id: int
    login_days: int
    content_views: int
    videos_completed: int
    points_earned: int
    items_exchanged: int
    sign_ins: int
    last_activity_at: Optional[datetime] = None
    behavior_stats: Dict[str, Any]

    class Config:
        from_attributes = True