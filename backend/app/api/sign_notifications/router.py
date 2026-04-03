from fastapi import APIRouter, Depends, HTTPException, Query, Security
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime, date
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import hashlib

from app.database import get_db
from app.models import User, SignRecord, Notification
from app.models.analytics import UserEngagement
from app.core.config import settings
from app.schemas.sign_notifications import (
    SignRecordResponse, 
    NotificationResponse, 
    MarkAsReadRequest,
    SignRewardResponse
)

router = APIRouter()

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)) -> User:
    """获取当前登录用户"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="认证失败")
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(status_code=401, detail="用户不存在")
        
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="认证失败")


@router.post("/sign-today", response_model=SignRewardResponse)
async def sign_today(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    今日签到
    """
    # 检查今天是否已签到
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    
    existing_sign = db.query(SignRecord).filter(
        SignRecord.user_id == current_user.id,
        SignRecord.sign_date >= today_start,
        SignRecord.sign_date <= today_end
    ).first()
    
    if existing_sign:
        raise HTTPException(status_code=400, detail="今日已签到")
    
    # 获取用户最近的签到记录以计算连续天数
    last_sign = db.query(SignRecord).filter(
        SignRecord.user_id == current_user.id
    ).order_by(SignRecord.sign_date.desc()).first()
    
    continuous_days = 1
    if last_sign:
        # 计算连续天数
        last_sign_date = last_sign.sign_date.date()
        today_date = date.today()
        
        if (today_date - last_sign_date).days == 1:
            # 连续签到
            continuous_days = last_sign.continuous_days + 1
        elif today_date == last_sign_date:
            # 今天已签到（理论上不应该发生）
            raise HTTPException(status_code=400, detail="今日已签到")
        else:
            # 断签，重新开始计数
            continuous_days = 1
    
    # 根据连续签到天数计算奖励积分
    base_points = 50
    bonus_points = min(continuous_days - 1, 10) * 5  # 最多增加50积分奖励
    total_points = base_points + bonus_points
    
    # 创建签到记录
    sign_record = SignRecord(
        user_id=current_user.id,
        points_awarded=total_points,
        continuous_days=continuous_days
    )
    db.add(sign_record)
    db.commit()
    db.refresh(sign_record)
    
    # 更新用户积分账户
    from app.models.points import UserPointAccount
    point_account = db.query(UserPointAccount).filter(UserPointAccount.user_id == current_user.id).first()
    if not point_account:
        point_account = UserPointAccount(user_id=current_user.id)
        db.add(point_account)
        db.commit()
        db.refresh(point_account)
    
    point_account.total_points += total_points
    point_account.available_points += total_points
    db.commit()
    
    # 更新用户参与度
    engagement = db.query(UserEngagement).filter(UserEngagement.user_id == current_user.id).first()
    if not engagement:
        engagement = UserEngagement(user_id=current_user.id)
        db.add(engagement)
    
    engagement.sign_ins = (engagement.sign_ins or 0) + 1
    engagement.last_activity_at = datetime.utcnow()
    db.commit()
    
    # 创建签到奖励通知
    notification = Notification(
        user_id=current_user.id,
        title="签到奖励到账",
        content=f"您今日签到获得{total_points}积分奖励，连续签到{continuous_days}天！",
        notification_type="points",
        related_id=str(sign_record.id)
    )
    db.add(notification)
    db.commit()
    
    return SignRewardResponse(
        success=True,
        points_awarded=total_points,
        continuous_days=continuous_days,
        message=f"签到成功！获得{total_points}积分"
    )


@router.get("/sign-info", response_model=dict)
async def get_sign_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取签到信息
    """
    # 获取今天是否已签到
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    
    today_signed = db.query(SignRecord).filter(
        SignRecord.user_id == current_user.id,
        SignRecord.sign_date >= today_start,
        SignRecord.sign_date <= today_end
    ).first() is not None
    
    # 获取连续签到天数
    current_streak = 0
    last_sign = db.query(SignRecord).filter(
        SignRecord.user_id == current_user.id
    ).order_by(SignRecord.sign_date.desc()).first()
    
    if last_sign:
        # 检查是否连续
        last_sign_date = last_sign.sign_date.date()
        today_date = date.today()
        
        if (today_date - last_sign_date).days == 0:
            # 今天已签到
            current_streak = last_sign.continuous_days
        elif (today_date - last_sign_date).days == 1:
            # 昨天签到，今天未签到
            current_streak = last_sign.continuous_days
        else:
            # 已断签
            current_streak = 0
    
    # 获取历史签到统计
    total_signed = db.query(SignRecord).filter(
        SignRecord.user_id == current_user.id
    ).count()
    
    # 获取最长连续签到
    longest_streak_result = db.execute(text("""
        SELECT MAX(continuous_days) FROM sign_records WHERE user_id = :user_id
    """), {"user_id": current_user.id}).fetchone()
    longest_streak = longest_streak_result[0] or 0
    
    return {
        "today_signed": today_signed,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_signed": total_signed
    }


@router.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    notification_type: Optional[str] = Query(None, description="通知类型: system, points, promotion"),
    is_read: Optional[bool] = Query(None, description="是否已读"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """
    获取用户的通知列表
    """
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if notification_type:
        query = query.filter(Notification.notification_type == notification_type)
    
    if is_read is not None:
        query = query.filter(Notification.is_read == is_read)
    
    notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    return notifications


@router.put("/notifications/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    标记通知为已读
    """
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="通知不存在")
    
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.commit()
    
    return {"message": "通知已标记为已读"}


@router.put("/notifications/mark-all-read")
async def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    标记所有通知为已读
    """
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({"is_read": True, "read_at": datetime.utcnow()})
    db.commit()
    
    return {"message": "所有通知已标记为已读"}


@router.get("/unread-count", response_model=int)
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取未读通知数量
    """
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()
    
    return count