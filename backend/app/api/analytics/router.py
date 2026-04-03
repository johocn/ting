from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta
import json

from app.database import get_db
from app.models import User
from app.models.analytics import UserBehavior, ConversionRate, UserEngagement
from app.core.security import get_current_user
from app.schemas.analytics import (
    UserBehaviorResponse,
    ConversionRateResponse,
    UserEngagementResponse,
    AnalyticsSummaryResponse,
    UserBehaviorCreate
)

router = APIRouter()


@router.post("/behavior/track")
async def track_user_behavior(
    behavior: UserBehaviorCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    追踪用户行为
    """
    behavior_record = UserBehavior(
        user_id=current_user.id,
        action_type=behavior.action_type,
        action_target=behavior.action_target,
        action_value=behavior.action_value,
        session_id=behavior.session_id,
        ip_address=behavior.ip_address,
        user_agent=behavior.user_agent,
        referrer=behavior.referrer
    )
    db.add(behavior_record)
    db.commit()
    db.refresh(behavior_record)
    
    # 更新用户参与度
    engagement = db.query(UserEngagement).filter(UserEngagement.user_id == current_user.id).first()
    if not engagement:
        engagement = UserEngagement(user_id=current_user.id)
        db.add(engagement)
    
    # 根据行为类型更新参与度指标
    if behavior.action_type == "login":
        engagement.login_days = func.coalesce(engagement.login_days, 0) + 1
    elif behavior.action_type == "view_content":
        engagement.content_views = func.coalesce(engagement.content_views, 0) + 1
    elif behavior.action_type == "complete_video":
        engagement.videos_completed = func.coalesce(engagement.videos_completed, 0) + 1
    elif behavior.action_type == "earn_points":
        engagement.points_earned = func.coalesce(engagement.points_earned, 0) + (behavior.action_value or 0)
    elif behavior.action_type == "exchange_item":
        engagement.items_exchanged = func.coalesce(engagement.items_exchanged, 0) + 1
    elif behavior.action_type == "sign_in":
        engagement.sign_ins = func.coalesce(engagement.sign_ins, 0) + 1
    
    engagement.last_activity_at = datetime.utcnow()
    db.commit()
    
    return {"message": "行为已记录", "id": behavior_record.id}


@router.get("/behaviors", response_model=List[UserBehaviorResponse])
async def get_user_behaviors(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    action_type: Optional[str] = Query(None, description="行为类型过滤"),
    start_date: Optional[datetime] = Query(None, description="开始时间"),
    end_date: Optional[datetime] = Query(None, description="结束时间"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """
    获取用户行为记录
    """
    query = db.query(UserBehavior).filter(UserBehavior.user_id == current_user.id)
    
    if action_type:
        query = query.filter(UserBehavior.action_type == action_type)
    
    if start_date:
        query = query.filter(UserBehavior.created_at >= start_date)
    
    if end_date:
        query = query.filter(UserBehavior.created_at <= end_date)
    
    behaviors = query.order_by(UserBehavior.created_at.desc()).offset(skip).limit(limit).all()
    
    return behaviors


@router.get("/analytics/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户数据分析摘要
    """
    # 获取用户参与度数据
    engagement = db.query(UserEngagement).filter(UserEngagement.user_id == current_user.id).first()
    
    if not engagement:
        engagement = UserEngagement(user_id=current_user.id)
    
    # 计算最近7天的行为统计
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_behaviors = db.query(UserBehavior).filter(
        and_(
            UserBehavior.user_id == current_user.id,
            UserBehavior.created_at >= seven_days_ago
        )
    ).all()
    
    # 按类型统计
    behavior_stats = {}
    for behavior in recent_behaviors:
        if behavior.action_type not in behavior_stats:
            behavior_stats[behavior.action_type] = 0
        behavior_stats[behavior.action_type] += 1
    
    return AnalyticsSummaryResponse(
        user_id=current_user.id,
        login_days=engagement.login_days or 0,
        content_views=engagement.content_views or 0,
        videos_completed=engagement.videos_completed or 0,
        points_earned=engagement.points_earned or 0,
        items_exchanged=engagement.items_exchanged or 0,
        sign_ins=engagement.sign_ins or 0,
        last_activity_at=engagement.last_activity_at,
        behavior_stats=behavior_stats
    )


@router.get("/analytics/popular-contents")
async def get_popular_contents(
    db: Session = Depends(get_db),
    days: int = Query(30, description="统计天数"),
    limit: int = Query(10, description="返回数量")
):
    """
    获取热门内容统计
    """
    from app.models.learning_progress import UserLearningSession
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # 从学习会话中获取热门内容
    popular_contents = db.query(
        UserLearningSession.content_id,
        func.count(UserLearningSession.id).label('view_count'),
        func.avg(UserLearningSession.progress_percentage).label('avg_completion_rate')
    ).filter(
        UserLearningSession.created_at >= start_date
    ).group_by(UserLearningSession.content_id).order_by(
        func.count(UserLearningSession.id).desc()
    ).limit(limit).all()
    
    # 获取内容详细信息
    from app.models.contents import Content
    results = []
    for content_id, view_count, avg_completion_rate in popular_contents:
        content = db.query(Content).filter(Content.id == content_id).first()
        if content:
            results.append({
                "content_id": content_id,
                "title": content.title,
                "category": content.category,
                "view_count": view_count,
                "avg_completion_rate": float(avg_completion_rate) if avg_completion_rate else 0
            })
    
    return results


@router.get("/analytics/conversion-funnel")
async def get_conversion_funnel(
    db: Session = Depends(get_db),
    days: int = Query(30, description="统计天数")
):
    """
    获取转化漏斗数据
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # 计算关键转化步骤
    total_users = db.query(User).count()
    
    users_logged_in = db.query(User).join(UserBehavior).filter(
        and_(
            UserBehavior.action_type == 'login',
            UserBehavior.created_at >= start_date
        )
    ).distinct().count()
    
    users_viewed_content = db.query(User).join(UserBehavior).filter(
        and_(
            UserBehavior.action_type == 'view_content',
            UserBehavior.created_at >= start_date
        )
    ).distinct().count()
    
    users_earned_points = db.query(User).join(UserBehavior).filter(
        and_(
            UserBehavior.action_type == 'earn_points',
            UserBehavior.created_at >= start_date
        )
    ).distinct().count()
    
    users_exchanged_items = db.query(User).join(UserBehavior).filter(
        and_(
            UserBehavior.action_type == 'exchange_item',
            UserBehavior.created_at >= start_date
        )
    ).distinct().count()
    
    return {
        "total_users": total_users,
        "logged_in": users_logged_in,
        "viewed_content": users_viewed_content,
        "earned_points": users_earned_points,
        "exchanged_items": users_exchanged_items,
        "conversion_rates": {
            "login_rate": round((users_logged_in / total_users * 100) if total_users > 0 else 0, 2),
            "content_view_rate": round((users_viewed_content / users_logged_in * 100) if users_logged_in > 0 else 0, 2),
            "earning_rate": round((users_earned_points / users_viewed_content * 100) if users_viewed_content > 0 else 0, 2),
            "exchange_rate": round((users_exchanged_items / users_earned_points * 100) if users_earned_points > 0 else 0, 2)
        }
    }


@router.get("/analytics/user-engagement")
async def get_user_engagement_overview(
    db: Session = Depends(get_db),
    days: int = Query(30, description="统计天数")
):
    """
    获取用户参与度概览
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # 按日期统计活跃用户数
    daily_active_users = db.query(
        func.date(UserBehavior.created_at).label('date'),
        func.count(UserBehavior.user_id.distinct()).label('active_users')
    ).filter(
        UserBehavior.created_at >= start_date
    ).group_by(func.date(UserBehavior.created_at)).order_by('date').all()
    
    # 统计各种行为的数量
    behavior_counts = db.query(
        UserBehavior.action_type,
        func.count(UserBehavior.id).label('count')
    ).filter(
        UserBehavior.created_at >= start_date
    ).group_by(UserBehavior.action_type).all()
    
    return {
        "daily_active_users": [
            {"date": str(dau[0]), "active_users": dau[1]} for dau in daily_active_users
        ],
        "behavior_counts": [
            {"action_type": bc[0], "count": bc[1]} for bc in behavior_counts
        ]
    }