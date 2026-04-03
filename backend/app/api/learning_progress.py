from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
import hashlib
from app.database import get_db
from app.models.contents import Content
from app.models.points import UserPointAccount, PointTransaction
from app.models.learning_progress import UserLearningSession
from app.services.point_calculator import calculate_watch_video_points

router = APIRouter(prefix="/learning", tags=["learning"])

@router.post("/start-learning", response_model=Dict)
async def start_learning(content_id: int, db: Session = Depends(get_db)):
    """开始学习（视频/音频）"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 获取内容信息
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")
    
    # 生成学习会话ID
    session_id = hashlib.md5(f"{user_id}_{content_id}_{datetime.now()}".encode()).hexdigest()
    
    # 创建学习会话记录
    learning_session = UserLearningSession(
        user_id=user_id,
        content_id=content_id,
        session_id=session_id,
        total_duration=content.duration,
        watched_duration=0,
        status="in_progress",
        progress_percentage=0
    )
    
    db.add(learning_session)
    db.commit()
    db.refresh(learning_session)
    
    return {
        "session_id": session_id,
        "message": "学习会话已开始",
        "start_time": learning_session.start_time.isoformat(),
        "content": {
            "id": content.id,
            "title": content.title,
            "duration": content.duration,
            "url": content.url,
            "reward_points_per_minute": content.reward_points_per_minute
        }
    }

@router.post("/update-progress", response_model=Dict)
async def update_learning_progress(
    session_id: str, 
    watched_duration: int, 
    db: Session = Depends(get_db)
):
    """更新学习进度（视频/音频观看时长）"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 获取学习会话记录
    learning_session = db.query(UserLearningSession).filter(
        UserLearningSession.session_id == session_id
    ).first()
    
    if not learning_session:
        raise HTTPException(status_code=404, detail="学习会话不存在")
    
    if learning_session.user_id != user_id:
        raise HTTPException(status_code=403, detail="无权访问此学习会话")
    
    # 更新观看时长
    learning_session.watched_duration = min(watched_duration, learning_session.total_duration)
    learning_session.updated_at = datetime.utcnow()
    
    # 计算学习进度百分比
    progress_percentage = 0
    if learning_session.total_duration > 0:
        progress_percentage = int((learning_session.watched_duration / learning_session.total_duration) * 100)
    
    learning_session.progress_percentage = progress_percentage
    
    db.commit()
    
    return {
        "session_id": session_id,
        "watched_duration": learning_session.watched_duration,
        "total_duration": learning_session.total_duration,
        "progress_percentage": progress_percentage,
        "message": "学习进度已更新"
    }

@router.post("/complete-learning", response_model=Dict)
async def complete_learning(session_id: str, db: Session = Depends(get_db)):
    """完成学习（计算并发放积分）"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 获取学习会话记录
    learning_session = db.query(UserLearningSession).filter(
        UserLearningSession.session_id == session_id
    ).first()
    
    if not learning_session:
        raise HTTPException(status_code=404, detail="学习会话不存在")
    
    if learning_session.user_id != user_id:
        raise HTTPException(status_code=403, detail="无权访问此学习会话")
    
    if learning_session.status == "completed":
        raise HTTPException(status_code=400, detail="学习已经完成")
    
    # 获取内容信息
    content = db.query(Content).filter(Content.id == learning_session.content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")
    
    # 计算获得的积分
    points_earned = calculate_watch_video_points(
        duration_seconds=learning_session.watched_duration,
        rate_per_minute=content.reward_points_per_minute
    )
    
    # 更新用户积分
    user_account = db.query(UserPointAccount).filter(
        UserPointAccount.user_id == user_id
    ).first()
    
    if not user_account:
        user_account = UserPointAccount(
            user_id=user_id,
            total_points=0,
            available_points=0,
            frozen_points=0,
            expired_points=0
        )
        db.add(user_account)
        db.commit()
        db.refresh(user_account)
    
    # 更新积分
    user_account.available_points = (user_account.available_points or 0) + points_earned
    user_account.total_points = (user_account.total_points or 0) + points_earned
    
    # 创建积分流水记录
    transaction = PointTransaction(
        user_id=user_id,
        transaction_type='earn',
        operation_type='watch_content',
        points_change=points_earned,
        balance_before=user_account.available_points - points_earned,
        balance_after=user_account.available_points,
        related_id=content.id,
        description=f'观看内容《{content.title}》获得积分',
        status='completed'
    )
    
    # 更新学习会话状态
    learning_session.status = "completed"
    learning_session.end_time = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    
    return {
        "session_id": session_id,
        "watched_duration": learning_session.watched_duration,
        "points_earned": points_earned,
        "total_points": user_account.available_points,
        "message": "学习完成，积分已发放"
    }

@router.get("/user-progress", response_model=List[Dict])
async def get_user_learning_progress(db: Session = Depends(get_db)):
    """获取用户的学习进度"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 获取用户的所有学习会话记录
    user_sessions = db.query(UserLearningSession).filter(
        UserLearningSession.user_id == user_id
    ).all()
    
    results = []
    for session in user_sessions:
        content = db.query(Content).filter(Content.id == session.content_id).first()
        if content:
            results.append({
                "session_id": session.session_id,
                "content": {
                    "id": content.id,
                    "title": content.title,
                    "duration": content.duration,
                    "category": content.category
                },
                "watched_duration": session.watched_duration,
                "progress_percentage": session.progress_percentage,
                "status": session.status,
                "start_time": session.start_time.isoformat() if session.start_time else None,
                "end_time": session.end_time.isoformat() if session.end_time else None,
                "total_duration": session.total_duration
            })
    
    return results

@router.get("/content-progress/{content_id}", response_model=Dict)
async def get_content_learning_progress(content_id: int, db: Session = Depends(get_db)):
    """获取特定内容的学习统计"""
    # 获取内容信息
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")
    
    # 获取该内容的学习统计
    from sqlalchemy import func
    total_sessions = db.query(UserLearningSession).filter(
        UserLearningSession.content_id == content_id
    ).count()
    
    completed_sessions = db.query(UserLearningSession).filter(
        UserLearningSession.content_id == content_id,
        UserLearningSession.status == "completed"
    ).count()
    
    avg_duration = db.query(func.avg(UserLearningSession.watched_duration)).filter(
        UserLearningSession.content_id == content_id
    ).scalar() or 0
    
    # 计算总积分发放量（通过积分流水记录）
    total_points = db.query(func.sum(PointTransaction.points_change)).filter(
        PointTransaction.operation_type == 'watch_content',
        PointTransaction.related_id == content_id
    ).scalar() or 0
    
    completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
    
    return {
        "content_id": content.id,
        "title": content.title,
        "total_learners": total_sessions,
        "completion_rate": round(completion_rate, 2),
        "average_duration": int(avg_duration),
        "total_points_distributed": total_points
    }