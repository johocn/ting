"""
内容API测试
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.users import User
from app.models.contents import Content, Question, ContentQuizConfig
from app.database import get_db
from unittest.mock import Mock

def test_create_content(test_client: TestClient, db_session):
    """测试创建内容"""
    # 创建测试用户
    user = User(
        username="testcontentuser",
        password_hash="password123",
        phone="13800138009"
    )
    db_session.add(user)
    db_session.commit()
    
    # 创建内容
    content_data = {
        "title": "测试视频内容",
        "url": "https://example.com/test.mp4",
        "duration": 1800,
        "category": "education",
        "reward_points_per_minute": 5,
        "status": True
    }
    
    response = test_client.post("/api/v1/contents/contents/", json=content_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "测试视频内容"
    assert data["duration"] == 1800
    assert data["category"] == "education"

def test_get_contents(test_client: TestClient, db_session):
    """测试获取内容列表"""
    # 首先创建一些测试内容
    content1 = Content(
        title="内容测试1",
        url="https://example.com/test1.mp4",
        duration=1800,
        category="education",
        reward_points_per_minute=5,
        status=True
    )
    content2 = Content(
        title="内容测试2",
        url="https://example.com/test2.mp4",
        duration=2400,
        category="technology",
        reward_points_per_minute=3,
        status=True
    )
    
    db_session.add(content1)
    db_session.add(content2)
    db_session.commit()
    
    response = test_client.get("/api/v1/contents/contents/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    
    # 检查是否包含创建的内容
    titles = [item["title"] for item in data]
    assert "内容测试1" in titles
    assert "内容测试2" in titles

def test_get_single_content(test_client: TestClient, db_session):
    """测试获取单个内容"""
    # 创建测试内容
    content = Content(
        title="单项测试内容",
        url="https://example.com/single-test.mp4",
        duration=1200,
        category="tutorial",
        reward_points_per_minute=4,
        status=True
    )
    db_session.add(content)
    db_session.commit()
    
    content_id = content.id
    
    response = test_client.get(f"/api/v1/contents/contents/{content_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == content_id
    assert data["title"] == "单项测试内容"
    assert data["duration"] == 1200

def test_update_content(test_client: TestClient, db_session):
    """测试更新内容"""
    # 创建测试内容
    content = Content(
        title="待更新内容",
        url="https://example.com/to-update.mp4",
        duration=1200,
        category="original",
        reward_points_per_minute=4,
        status=True
    )
    db_session.add(content)
    db_session.commit()
    
    content_id = content.id
    
    # 更新数据
    update_data = {
        "title": "已更新内容",
        "category": "updated",
        "duration": 1800
    }
    
    response = test_client.put(f"/api/v1/contents/contents/{content_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == content_id
    assert data["title"] == "已更新内容"
    assert data["category"] == "updated"
    assert data["duration"] == 1800

def test_delete_content(test_client: TestClient, db_session):
    """测试删除内容"""
    # 创建测试内容
    content = Content(
        title="待删除内容",
        url="https://example.com/to-delete.mp4",
        duration=1200,
        category="to-be-deleted",
        reward_points_per_minute=4,
        status=True
    )
    db_session.add(content)
    db_session.commit()
    
    content_id = content.id
    
    # 删除内容
    response = test_client.delete(f"/api/v1/contents/contents/{content_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "内容删除成功"
    
    # 验证内容已被删除
    get_response = test_client.get(f"/api/v1/contents/contents/{content_id}")
    assert get_response.status_code == 404

def test_content_with_questions(test_client: TestClient, db_session):
    """测试内容与问题的关联"""
    # 创建测试内容
    content = Content(
        title="带问题的测试内容",
        url="https://example.com/with-questions.mp4",
        duration=1200,
        category="education",
        reward_points_per_minute=5,
        status=True
    )
    db_session.add(content)
    db_session.commit()
    
    content_id = content.id
    
    # 创建问题
    question_data = {
        "question_text": "这是一个测试问题吗？",
        "options": ["是", "否", "不确定"],
        "correct_answer": "是",
        "individual_points": 10,
        "question_order": 1
    }
    
    response = test_client.post(f"/api/v1/contents/contents/{content_id}/questions", json=question_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["question_text"] == "这是一个测试问题吗？"
    
    # 获取内容的问题列表
    get_questions_response = test_client.get(f"/api/v1/contents/contents/{content_id}/questions")
    assert get_questions_response.status_code == 200
    questions_data = get_questions_response.json()
    assert isinstance(questions_data, list)
    assert len(questions_data) == 1
    assert questions_data[0]["question_text"] == "这是一个测试问题吗？"

def test_content_quiz_config(test_client: TestClient, db_session):
    """测试内容答题配置"""
    # 创建测试内容
    content = Content(
        title="带配置的测试内容",
        url="https://example.com/with-config.mp4",
        duration=1800,
        category="education",
        reward_points_per_minute=5,
        status=True
    )
    db_session.add(content)
    db_session.commit()
    
    content_id = content.id
    
    # 设置答题配置
    config_data = {
        "total_questions": 10,
        "required_correct": 8,
        "pass_percentage": 80,
        "quiz_points": 100,
        "time_limit": 1800,
        "allow_retry": True,
        "retry_limit": 3
    }
    
    response = test_client.put(f"/api/v1/contents/contents/{content_id}/quiz-config", json=config_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["content_id"] == content_id
    assert data["total_questions"] == 10
    assert data["quiz_points"] == 100
    
    # 获取答题配置
    get_config_response = test_client.get(f"/api/v1/contents/contents/{content_id}/quiz-config")
    assert get_config_response.status_code == 200
    config_data = get_config_response.json()
    assert config_data["content_id"] == content_id
    assert config_data["total_questions"] == 10
    assert config_data["quiz_points"] == 100