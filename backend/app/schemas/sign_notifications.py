from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SignRecordResponse(BaseModel):
    id: int
    user_id: int
    sign_date: datetime
    points_awarded: int
    continuous_days: int
    is_reward_claimed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    notification_type: str
    related_id: Optional[str] = None
    is_read: bool
    priority: int
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MarkAsReadRequest(BaseModel):
    notification_ids: list[int]


class SignRewardResponse(BaseModel):
    success: bool
    points_awarded: int
    continuous_days: int
    message: str