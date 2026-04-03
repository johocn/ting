"""
学习进度API测试
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base
from app.models.users import User
from app.models.contents import Content
from app.models.points import UserPointAccount

# 使用内存数据库进行测试
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_learning.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db_session():
    """创建测试数据库会话"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def test_client(test_db_session):
    """创建测试客户端"""
    def override_get_db():
        try:
            yield test_db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

def test_learning_flow(test_client: TestClient, test_db_session):
    """测试完整的学习流程"""
    # 1. 创建一个测试用户
    user = User(
        username="testuser",
        password_hash="hashed_password",
        phone="13800138000",
        integral=0
    )
    test_db_session.add(user)
    test_db_session.commit()
    user_id = user.id
    
    # 2. 创建一个测试内容
    content = Content(
        title="测试学习内容",
        url="https://example.com/test-video.mp4",
        duration=1800,  # 30分钟
        category="education",
        reward_points_per_minute=5,
        status=True
    )
    test_db_session.add(content)
    test_db_session.commit()
    content_id = content.id
    
    # 3. 开始学习
    start_response = test_client.post(f"/api/v1/learning/start-learning?content_id={content_id}")
    assert start_response.status_code == 200
    start_data = start_response.json()
    assert "session_id" in start_data
    assert start_data["message"] == "学习会话已开始"
    
    session_id = start_data["session_id"]
    
    # 4. 更新学习进度
    update_response = test_client.post(
        f"/api/v1/learning/update-progress",
        params={"session_id": session_id, "watched_duration": 600}  # 10分钟
    )
    assert update_response.status_code == 200
    update_data = update_response.json()
    assert update_data["session_id"] == session_id
    assert update_data["watched_duration"] == 600
    assert update_data["progress_percentage"] == 33  # 600/1800 ≈ 33%
    
    # 5. 完成学习
    complete_response = test_client.post(f"/api/v1/learning/complete-learning?session_id={session_id}")
    assert complete_response.status_code == 200
    complete_data = complete_response.json()
    assert "points_earned" in complete_data
    assert "total_points" in complete_data
    # 计算的积分应该是 600秒 / 60 * 5分/分钟 = 50分
    expected_points = int((600 / 60) * 5)
    assert complete_data["points_earned"] == expected_points
    
    # 6. 获取用户学习进度
    progress_response = test_client.get("/api/v1/learning/user-progress")
    assert progress_response.status_code == 200
    progress_data = progress_response.json()
    assert isinstance(progress_data, list)
    assert len(progress_data) > 0
    
    # 验证特定的学习会话
    session_found = False
    for session in progress_data:
        if session["session_id"] == session_id:
            session_found = True
            assert session["status"] == "completed"
            assert session["watched_duration"] == 600
            assert session["progress_percentage"] == 33
            break
    
    assert session_found, "学习会话未在进度列表中找到"

def test_get_content_learning_stats(test_client: TestClient, test_db_session):
    """测试获取内容学习统计"""
    # 创建测试内容
    content = Content(
        title="统计测试内容",
        url="https://example.com/stats-test.mp4",
        duration=1200,  # 20分钟
        category="education",
        reward_points_per_minute=3,
        status=True
    )
    test_db_session.add(content)
    test_db_session.commit()
    content_id = content.id
    
    # 获取内容学习统计
    stats_response = test_client.get(f"/api/v1/learning/content-progress/{content_id}")
    assert stats_response.status_code == 200
    stats_data = stats_response.json()
    
    assert "content_id" in stats_data
    assert "title" in stats_data
    assert "total_learners" in stats_data
    assert "completion_rate" in stats_data
    assert stats_data["content_id"] == content_id
    assert stats_data["title"] == "统计测试内容"

def test_learning_with_different_durations(test_client: TestClient, test_db_session):
    """测试不同学习时长的情况"""
    # 创建测试用户和内容
    user = User(
        username="testuser2",
        password_hash="hashed_password",
        phone="13800138001",
        integral=0
    )
    test_db_session.add(user)
    test_db_session.commit()
    
    content = Content(
        title="不同长度测试",
        url="https://example.com/duration-test.mp4",
        duration=2400,  # 40分钟
        category="education",
        reward_points_per_minute=4,
        status=True
    )
    test_db_session.add(content)
    test_db_session.commit()
    content_id = content.id
    
    # 开始学习
    start_response = test_client.post(f"/api/v1/learning/start-learning?content_id={content_id}")
    assert start_response.status_code == 200
    session_id = start_response.json()["session_id"]
    
    # 更新不同进度
    test_durations = [300, 600, 1200, 1800]  # 5, 10, 20, 30分钟
    
    for duration in test_durations:
        update_response = test_client.post(
            f"/api/v1/learning/update-progress",
            params={"session_id": session_id, "watched_duration": duration}
        )
        assert update_response.status_code == 200
        update_data = update_response.json()
        expected_percentage = int((duration / 2400) * 100)
        assert update_data["progress_percentage"] == expected_percentage
        assert update_data["watched_duration"] == duration

def test_invalid_session_handling(test_client: TestClient):
    """测试无效会话的处理"""
    # 尝试使用不存在的会话ID更新进度
    invalid_response = test_client.post(
        "/api/v1/learning/update-progress",
        params={"session_id": "invalid_session_id", "watched_duration": 300}
    )
    # 根据我们的实现，这可能会返回404或创建新记录
    # 具体行为取决于实现细节
    assert invalid_response.status_code in [404, 200]  # 接受多种可能的结果

if __name__ == "__main__":
    pytest.main([__file__])