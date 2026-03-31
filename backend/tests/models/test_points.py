import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.users import User
from app.models.points import UserPointAccount, PointTransaction, PointExpirationRule

class TestPointModel:
    """积分模型测试"""
    
    def test_create_user_point_account(self, db_session: Session):
        """测试创建用户积分账户"""
        user = User(username="testuser", password_hash="hashed_password", phone="13800138000")
        db_session.add(user)
        db_session.commit()
        
        account = UserPointAccount(
            user_id=user.id,
            total_points=100,
            available_points=80,
            frozen_points=20,
            expired_points=0
        )
        db_session.add(account)
        db_session.commit()
        
        assert account.id is not None
        assert account.user_id == user.id
        assert account.total_points == 100
        assert account.available_points == 80
        assert account.frozen_points == 20
        assert account.expired_points == 0
    
    def test_create_point_transaction(self, db_session: Session):
        """测试创建积分流水"""
        user = User(username="testuser2", password_hash="hashed_password", phone="13800138001")
        db_session.add(user)
        db_session.commit()
        
        transaction = PointTransaction(
            user_id=user.id,
            transaction_type="earn",
            operation_type="watch_video",
            points_change=50,
            balance_before=0,
            balance_after=50,
            description="观看视频奖励",
            status="active"
        )
        db_session.add(transaction)
        db_session.commit()
        
        assert transaction.id is not None
        assert transaction.user_id == user.id
        assert transaction.transaction_type == "earn"
        assert transaction.operation_type == "watch_video"
        assert transaction.points_change == 50
        assert transaction.balance_before == 0
        assert transaction.balance_after == 50
        assert transaction.description == "观看视频奖励"
        assert transaction.status == "active"
    
    def test_point_expiration_rule(self, db_session: Session):
        """测试积分过期规则"""
        rule = PointExpirationRule(
            rule_name="一年有效期",
            validity_period_days=365,
            apply_to_new=True,
            is_active=True
        )
        db_session.add(rule)
        db_session.commit()
        
        assert rule.id is not None
        assert rule.rule_name == "一年有效期"
        assert rule.validity_period_days == 365
        assert rule.apply_to_new == True
        assert rule.is_active == True
    
    def test_point_transaction_with_expiration(self, db_session: Session):
        """测试带过期时间的积分流水"""
        user = User(username="testuser3", password_hash="hashed_password", phone="13800138002")
        db_session.add(user)
        db_session.commit()
        
        expiration_date = datetime.utcnow() + timedelta(days=30)
        
        transaction = PointTransaction(
            user_id=user.id,
            transaction_type="earn",
            operation_type="answer_quiz",
            points_change=100,
            balance_before=0,
            balance_after=100,
            description="答题奖励",
            expiration_date=expiration_date,
            status="active"
        )
        db_session.add(transaction)
        db_session.commit()
        
        assert transaction.id is not None
        assert transaction.expiration_date == expiration_date
        assert transaction.status == "active"
