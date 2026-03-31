import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.users import User
from app.models.points import UserPointAccount
from sqlalchemy.orm import Session

class TestAuthAPI:
    """认证API测试"""
    
    def test_register_user(self, client: TestClient, db_session: Session):
        """测试用户注册"""
        response = client.post("/api/v1/auth/register", json={
            "username": "testuser",
            "password": "password123",
            "phone": "13800138000"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "token" in data
        assert data["username"] == "testuser"
    
    def test_login_user(self, client: TestClient, db_session: Session):
        """测试用户登录"""
        # 先注册用户
        register_response = client.post("/api/v1/auth/register", json={
            "username": "testlogin",
            "password": "password123",
            "phone": "13800138001"
        })
        
        assert register_response.status_code == 200
        
        # 登录用户
        login_response = client.post("/api/v1/auth/login", json={
            "username": "testlogin",
            "password": "password123"
        })
        
        assert login_response.status_code == 200
        data = login_response.json()
        assert "user_id" in data
        assert "token" in data
        assert data["username"] == "testlogin"
    
    def test_login_invalid_credentials(self, client: TestClient, db_session: Session):
        """测试无效登录凭证"""
        response = client.post("/api/v1/auth/login", json={
            "username": "nonexistent",
            "password": "wrongpassword"
        })
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    def test_get_user_profile(self, client: TestClient, db_session: Session):
        """测试获取用户资料"""
        # 注册并登录用户
        register_response = client.post("/api/v1/auth/register", json={
            "username": "testprofile",
            "password": "password123",
            "phone": "13800138002"
        })
        
        assert register_response.status_code == 200
        token = register_response.json()["token"]
        
        # 获取用户资料
        response = client.get("/api/v1/users/profile", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testprofile"
        assert data["phone"] == "13800138002"
        assert data["integral"] >= 0  # 新用户应该有初始积分
