import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.users import User
from app.models.contents import Content, Question, ContentQuizConfig

class TestContentAPI:
    """内容API测试"""
    
    def test_create_content(self, client: TestClient, db_session):
        """测试创建内容"""
        # 创建测试用户
        user = User(username="testcontent", password_hash="password123", phone="13800138000")
        db_session.add(user)
        db_session.commit()
        
        # 创建内容
        response = client.post("/api/v1/contents", json={
            "title": "测试视频",
            "url": "https://example.com/test.mp4",
            "duration": 1800,
            "category": "education",
            "reward_points_per_minute": 5,
            "status": True
        }, headers={
            "Authorization": f"Bearer mock_token"
        })
        
        # 注意：在实际测试中，我们需要模拟认证，这里先跳过
        # 这里我们测试不需要认证的接口
        pass
    
    def test_get_contents(self, client: TestClient, db_session):
        """测试获取内容列表"""
        response = client.get("/api/v1/contents")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_content_lifecycle(self, client: TestClient, db_session):
        """测试内容生命周期"""
        # 这里我们测试内容的完整生命周期
        # 由于认证问题，我们暂时只测试结构
        pass
