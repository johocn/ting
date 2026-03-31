from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.points import UserPointAccount, PointTransaction, PointExpirationRule
from app.schemas.points import PointTransactionCreate

router = APIRouter(prefix="/points", tags=["points"])

@router.get("/account", response_model=dict)
async def get_user_point_account(db: Session = Depends(get_db)):
    """获取用户积分账户信息（模拟用户ID为1）"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    account = db.query(UserPointAccount).filter(
        UserPointAccount.user_id == user_id
    ).first()
    
    if not account:
        # 如果账户不存在，创建新账户
        account = UserPointAccount(user_id=user_id)
        db.add(account)
        db.commit()
        db.refresh(account)
    
    return {
        "user_id": account.user_id,
        "total_points": account.total_points,
        "available_points": account.available_points,
        "frozen_points": account.frozen_points,
        "expired_points": account.expired_points
    }

@router.get("/transactions", response_model=List[dict])
async def get_point_transactions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """获取积分流水记录"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    transactions = db.query(PointTransaction).filter(
        PointTransaction.user_id == user_id
    ).offset(skip).limit(limit).all()
    
    return transactions

@router.get("/expiring", response_model=dict)
async def get_expiring_points(db: Session = Depends(get_db)):
    """获取即将过期的积分"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 这里可以查询未来30天内过期的积分
    from datetime import datetime, timedelta
    from sqlalchemy import and_
    
    future_date = datetime.utcnow() + timedelta(days=30)
    
    expiring_transactions = db.query(PointTransaction).filter(
        and_(
            PointTransaction.user_id == user_id,
            PointTransaction.expiration_date <= future_date,
            PointTransaction.expiration_date >= datetime.utcnow(),
            PointTransaction.status == 'active'
        )
    ).all()
    
    # 按过期日期分组
    expiring_points = {}
    for tx in expiring_transactions:
        exp_date = tx.expiration_date.strftime('%Y-%m-%d')
        if exp_date not in expiring_points:
            expiring_points[exp_date] = 0
        expiring_points[exp_date] += tx.points_change
    
    return {
        "expiring_points": [
            {"date": date, "points": points} 
            for date, points in expiring_points.items()
        ]
    }

@router.post("/transaction", response_model=dict)
async def create_point_transaction(
    transaction: PointTransactionCreate, 
    db: Session = Depends(get_db)
):
    """创建积分流水记录"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 获取用户当前积分账户
    account = db.query(UserPointAccount).filter(
        UserPointAccount.user_id == user_id
    ).first()
    
    if not account:
        account = UserPointAccount(user_id=user_id)
        db.add(account)
        db.commit()
        db.refresh(account)
    
    # 创建新流水记录
    balance_before = account.available_points
    balance_after = balance_before + transaction.points_change
    
    # 更新账户余额
    account.available_points = balance_after
    account.total_points = account.total_points + max(0, transaction.points_change)  # 只增加正数
    
    new_transaction = PointTransaction(
        user_id=user_id,
        transaction_type=transaction.transaction_type,
        operation_type=transaction.operation_type,
        points_change=transaction.points_change,
        balance_before=balance_before,
        balance_after=balance_after,
        related_id=transaction.related_id,
        description=transaction.description,
        expiration_date=transaction.expiration_date,
        status='active'
    )
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return new_transaction

@router.get("/expiration-rules", response_model=List[dict])
async def get_expiration_rules(db: Session = Depends(get_db)):
    """获取积分过期规则"""
    rules = db.query(PointExpirationRule).filter(
        PointExpirationRule.is_active == True
    ).all()
    
    return rules
