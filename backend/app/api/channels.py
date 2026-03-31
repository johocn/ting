from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.channels import (
    ChannelType, Channel, ChannelUserRelation, ChannelStatistics,
    ChannelPermission, ChannelPointConfig, ChannelHierarchy, ChannelInvitationRecord
)
from app.schemas.channels import ChannelCreate, ChannelUpdate

router = APIRouter(prefix="/channels", tags=["channels"])

@router.get("/types", response_model=List[dict])
async def get_channel_types(db: Session = Depends(get_db)):
    """获取渠道类型列表"""
    types = db.query(ChannelType).filter(ChannelType.is_active == True).all()
    return types

@router.get("/my", response_model=List[dict])
async def get_my_channels(db: Session = Depends(get_db)):
    """获取我的渠道列表（模拟用户ID为1）"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    channels = db.query(Channel).filter(
        Channel.creator_user_id == user_id
    ).all()
    
    result = []
    for channel in channels:
        # 获取统计信息
        stats = db.query(ChannelStatistics).filter(
            ChannelStatistics.channel_id == channel.id
        ).order_by(ChannelStatistics.date.desc()).first()
        
        result.append({
            "id": channel.id,
            "name": channel.name,
            "code": channel.code,
            "type_id": channel.type_id,
            "parent_channel_id": channel.parent_channel_id,
            "commission_rate": channel.commission_rate,
            "invite_link": channel.invite_link,
            "stats": {
                "registered_users": stats.registered_users if stats else 0,
                "active_users": stats.active_users if stats else 0
            },
            "created_at": channel.created_at,
            "is_active": channel.is_active
        })
    
    return result

@router.get("/", response_model=List[dict])
async def get_channels(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """获取渠道列表"""
    channels = db.query(Channel).offset(skip).limit(limit).all()
    return channels

@router.get("/{channel_id}", response_model=dict)
async def get_channel(channel_id: int, db: Session = Depends(get_db)):
    """获取单个渠道信息"""
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="渠道不存在")
    return channel

@router.post("/", response_model=dict)
async def create_channel(
    channel_data: ChannelCreate, 
    db: Session = Depends(get_db)
):
    """创建渠道"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 生成邀请码
    import random
    import string
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # 生成邀请链接
    invite_link = f"https://yourapp.com/register?channel={code}"
    
    db_channel = Channel(
        name=channel_data.name,
        code=code,
        type_id=channel_data.type_id,
        creator_user_id=user_id,
        parent_channel_id=channel_data.parent_channel_id,
        commission_rate=channel_data.commission_rate,
        invite_link=invite_link,
        settings=channel_data.settings or {}
    )
    
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    
    return db_channel

@router.put("/{channel_id}", response_model=dict)
async def update_channel(
    channel_id: int, 
    channel_update: ChannelUpdate, 
    db: Session = Depends(get_db)
):
    """更新渠道信息"""
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="渠道不存在")
    
    for key, value in channel_update.model_dump(exclude_unset=True).items():
        setattr(channel, key, value)
    
    db.commit()
    return channel

@router.delete("/{channel_id}")
async def delete_channel(channel_id: int, db: Session = Depends(get_db)):
    """删除渠道"""
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="渠道不存在")
    
    db.delete(channel)
    db.commit()
    return {"message": "渠道删除成功"}

@router.get("/{channel_id}/statistics", response_model=dict)
async def get_channel_statistics(
    channel_id: int, 
    start_date: str = None, 
    end_date: str = None, 
    db: Session = Depends(get_db)
):
    """获取渠道统计数据"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 检查权限：用户只能查看自己的渠道
    channel = db.query(Channel).filter(
        Channel.id == channel_id,
        Channel.creator_user_id == user_id
    ).first()
    
    if not channel:
        raise HTTPException(status_code=403, detail="无权限访问此渠道")
    
    # 构建查询
    query = db.query(ChannelStatistics).filter(
        ChannelStatistics.channel_id == channel_id
    )
    
    from datetime import datetime
    if start_date:
        query = query.filter(ChannelStatistics.date >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(ChannelStatistics.date <= datetime.fromisoformat(end_date))
    
    stats = query.all()
    
    # 计算汇总数据
    total_registered = sum(s.registered_users for s in stats)
    total_active = sum(s.active_users for s in stats)
    total_earned = sum(s.earned_points for s in stats)
    total_spent = sum(s.spent_points for s in stats)
    
    return {
        "channel_id": channel_id,
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "total_registered": total_registered,
        "total_active": total_active,
        "total_earned_points": total_earned,
        "total_spent_points": total_spent,
        "daily_stats": [
            {
                "date": s.date.isoformat(),
                "registered_users": s.registered_users,
                "active_users": s.active_users,
                "earned_points": s.earned_points,
                "spent_points": s.spent_points
            }
            for s in stats
        ]
    }

@router.get("/{channel_id}/users", response_model=List[dict])
async def get_channel_users(
    channel_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """获取渠道下的用户"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 检查权限
    channel = db.query(Channel).filter(
        Channel.id == channel_id,
        Channel.creator_user_id == user_id
    ).first()
    
    if not channel:
        raise HTTPException(status_code=403, detail="无权限访问此渠道")
    
    relations = db.query(ChannelUserRelation).filter(
        ChannelUserRelation.channel_id == channel_id
    ).offset(skip).limit(limit).all()
    
    users = []
    for relation in relations:
        user = db.query(User).filter(User.id == relation.user_id).first()
        if user:
            users.append({
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
                "integral": user.integral,
                "joined_at": relation.joined_at,
                "level": relation.level
            })
    
    return users
