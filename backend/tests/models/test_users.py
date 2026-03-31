import pytest
from sqlalchemy.orm import Session
from app.models.users import User
from app.models.points import UserPointAccount
from app.models.channels import ChannelUserRelation

class TestUserModel:
    """用户模型测试"""
    
    def test_create_user(self, db_session: Session):
        """测试创建用户"""
        user = User(
            username="testuser",
            password_hash="hashed_password",
            phone="13800138000",
            email="test@example.com",
            integral=100
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.username == "testuser"
        assert user.integral == 100
        assert user.created_at is not None
    
    def test_user_point_account_creation(self, db_session: Session):
        """测试用户积分账户自动创建"""
        user = User(
            username="testuser2",
            password_hash="hashed_password",
            phone="13800138001"
        )
        db_session.add(user)
        db_session.commit()
        
        # 验证用户积分账户是否自动创建
        point_account = db_session.query(UserPointAccount).filter(
            UserPointAccount.user_id == user.id
        ).first()
        
        assert point_account is not None
        assert point_account.user_id == user.id
        assert point_account.total_points == 0
        assert point_account.available_points == 0
    
    def test_user_channel_relation(self, db_session: Session):
        """测试用户渠道关系"""
        user = User(username="testuser3", password_hash="hashed_password", phone="13800138002")
        db_session.add(user)
        db_session.commit()
        
        # 创建渠道关系
        channel_relation = ChannelUserRelation(
            channel_id=1,
            user_id=user.id,
            level=1
        )
        db_session.add(channel_relation)
        db_session.commit()
        
        assert channel_relation.id is not None
        assert channel_relation.user_id == user.id
        assert channel_relation.level == 1

    def test_user_update_integral(self, db_session: Session):
        """测试用户积分更新"""
        user = User(
            username="testuser4",
            password_hash="hashed_password",
            phone="13800138003",
            integral=50
        )
        db_session.add(user)
        db_session.commit()
        
        # 更新积分
        user.integral += 100
        db_session.commit()
        
        updated_user = db_session.query(User).filter(User.id == user.id).first()
        assert updated_user.integral == 150
