from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PointTransactionBase(BaseModel):
    transaction_type: str  # earn/spend/freeze/thaw
    operation_type: str  # watch_video, answer_quiz, purchase, exchange
    points_change: int  # 积分变化量
    related_id: Optional[int] = None  # 相关记录ID
    description: Optional[str] = ""
    expiration_date: Optional[datetime] = None

class PointTransactionCreate(PointTransactionBase):
    pass

class PointTransactionUpdate(BaseModel):
    transaction_type: Optional[str] = None
    operation_type: Optional[str] = None
    points_change: Optional[int] = None
    related_id: Optional[int] = None
    description: Optional[str] = None
    expiration_date: Optional[datetime] = None
    status: Optional[str] = None

class PointExpirationRuleBase(BaseModel):
    rule_name: str
    validity_period_days: Optional[int] = 365
    apply_to_new: Optional[bool] = True

class PointExpirationRuleCreate(PointExpirationRuleBase):
    pass

class PointExpirationRuleUpdate(BaseModel):
    rule_name: Optional[str] = None
    validity_period_days: Optional[int] = None
    apply_to_new: Optional[bool] = None
    is_active: Optional[bool] = None
