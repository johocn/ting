from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.channels import Channel, ChannelPermission, ChannelPointConfig, ChannelStatistics, ChannelUserRelation
from app.models.users import User
from app.schemas.hierarchy import HierarchyLevelResponse

router = APIRouter(prefix="/hierarchy", tags=["hierarchy"])

@router.get("/{level_id}", response_model=HierarchyLevelResponse)
async def get_hierarchy_level(level_id: int, db: Session = Depends(get_db)):
    """获取层级信息"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 获取渠道信息
    channel = db.query(Channel).filter(Channel.id == level_id).first()
    
    if not channel:
        raise HTTPException(status_code=404, detail="层级不存在")
    
    # 检查权限：用户只能查看自己的渠道或下级渠道
    if not has_hierarchy_permission(user_id, level_id, db):
        raise HTTPException(status_code=403, detail="无权限访问此层级")
    
    # 获取权限
    permissions = db.query(ChannelPermission).filter(
        ChannelPermission.channel_id == level_id
    ).all()
    
    # 获取积分配置
    point_configs = db.query(ChannelPointConfig).filter(
        ChannelPointConfig.channel_id == level_id,
        ChannelPointConfig.is_active == True
    ).all()
    
    # 获取下属渠道
    subordinates = db.query(Channel).filter(
        Channel.parent_channel_id == level_id
    ).all()
    
    # 获取直属用户
    users = db.query(User).join(
        ChannelUserRelation
    ).filter(
        ChannelUserRelation.channel_id == level_id
    ).limit(20).all()
    
    return {
        "level": {
            "id": channel.id,
            "name": channel.name,
            "child_count": len(subordinates),
            "total_users": len(users)
        },
        "permissions": [
            {
                "code": p.permission_code,
                "name": p.permission_name,
                "enabled": p.is_allowed
            }
            for p in permissions
        ],
        "point_configs": [
            {
                "type": pc.config_type,
                "multiplier": pc.multiplier,
                "fixed_bonus": pc.fixed_bonus
            }
            for pc in point_configs
        ],
        "subordinates": [
            {
                "id": s.id,
                "name": s.name,
                "user_count": get_user_count_for_channel(s.id, db),
                "commission_rate": s.commission_rate
            }
            for s in subordinates
        ],
        "users": [
            {
                "id": u.id,
                "username": u.username,
                "points": get_user_points(u.id, db),
                "is_active": True  # 实际应从用户状态获取
            }
            for u in users
        ]
    }

@router.get("/{level_id}/statistics", response_model=dict)
async def get_hierarchy_statistics(level_id: int, db: Session = Depends(get_db)):
    """获取层级统计数据"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    if not has_hierarchy_permission(user_id, level_id, db):
        raise HTTPException(status_code=403, detail="无权限访问此层级")
    
    from datetime import datetime
    # 获取统计
    today_stats = db.query(ChannelStatistics).filter(
        ChannelStatistics.channel_id == level_id,
        ChannelStatistics.date == datetime.today().date()
    ).first()
    
    if not today_stats:
        today_stats = ChannelStatistics(
            channel_id=level_id,
            date=datetime.today().date()
        )
    
    return {
        "users": {
            "registered": today_stats.registered_users,
            "active": today_stats.active_users
        },
        "points": {
            "earned": today_stats.earned_points,
            "spent": today_stats.spent_points
        },
        "transactions": {
            "exchanges": today_stats.exchange_count,
            "verifications": today_stats.verification_count
        }
    }

@router.get("/{level_id}/subordinates", response_model=List[dict])
async def get_subordinates(level_id: int, db: Session = Depends(get_db)):
    """获取下级层级"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    if not has_hierarchy_permission(user_id, level_id, db):
        raise HTTPException(status_code=403, detail="无权限访问此层级")
    
    subordinates = db.query(Channel).filter(
        Channel.parent_channel_id == level_id
    ).all()
    
    result = []
    for sub in subordinates:
        # 获取统计信息
        stats = db.query(ChannelStatistics).filter(
            ChannelStatistics.channel_id == sub.id
        ).order_by(ChannelStatistics.date.desc()).first()
        
        result.append({
            "id": sub.id,
            "name": sub.name,
            "user_count": get_user_count_for_channel(sub.id, db),
            "commission_rate": sub.commission_rate,
            "stats": {
                "registered_users": stats.registered_users if stats else 0,
                "active_users": stats.active_users if stats else 0
            }
        })
    
    return result

@router.get("/{level_id}/users", response_model=List[dict])
async def get_direct_users(level_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取直属用户"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    if not has_hierarchy_permission(user_id, level_id, db):
        raise HTTPException(status_code=403, detail="无权限访问此层级")
    
    users = db.query(User).join(
        ChannelUserRelation
    ).filter(
        ChannelUserRelation.channel_id == level_id
    ).offset(skip).limit(limit).all()
    
    result = []
    for user in users:
        # 获取用户积分
        from app.models.points import UserPointAccount
        account = db.query(UserPointAccount).filter(
            UserPointAccount.user_id == user.id
        ).first()
        
        result.append({
            "id": user.id,
            "username": user.username,
            "phone": user.phone,
            "points": account.available_points if account else 0,
            "is_active": user.is_active,
            "created_at": user.created_at
        })
    
    return result

def has_hierarchy_permission(user_id: int, level_id: int, db: Session) -> bool:
    """检查用户是否有访问层级的权限"""
    # 获取用户创建的渠道
    from app.models.channels import Channel
    user_channels = db.query(Channel.id).filter(
        Channel.creator_user_id == user_id
    ).all()
    
    user_channel_ids = [ch.id for ch in user_channels]
    
    # 检查是否是用户自己的渠道或其下级渠道
    if level_id in user_channel_ids:
        return True
    
    # 检查是否是用户渠道的下级
    # 这里需要递归检查层级关系
    return is_subordinate_of_user_channels(level_id, user_channel_ids, db)

def is_subordinate_of_user_channels(level_id: int, user_channel_ids: list, db: Session) -> bool:
    """检查层级是否是用户渠道的下级"""
    current_id = level_id
    
    while current_id:
        channel = db.query(Channel).filter(Channel.id == current_id).first()
        if not channel:
            break
            
        if channel.parent_channel_id in user_channel_ids:
            return True
            
        current_id = channel.parent_channel_id
    
    return False

def get_user_count_for_channel(channel_id: int, db: Session) -> int:
    """获取渠道用户数量"""
    from app.models.channels import ChannelUserRelation
    return db.query(ChannelUserRelation).filter(
        ChannelUserRelation.channel_id == channel_id
    ).count()

def get_user_points(user_id: int, db: Session) -> int:
    """获取用户积分"""
    from app.models.points import UserPointAccount
    account = db.query(UserPointAccount).filter(
        UserPointAccount.user_id == user_id
    ).first()
    
    return account.available_points if account else 0
