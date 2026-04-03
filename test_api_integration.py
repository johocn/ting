"""
API端到端测试脚本
"""
import requests
import json
import time

def test_api_endpoints():
    """测试API端点连通性"""
    base_url = "http://localhost:8000"
    
    print("测试API端点连通性...")
    
    # 测试根路径
    try:
        response = requests.get(f"{base_url}/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("✓ 根路径测试通过")
    except Exception as e:
        print(f"✗ 根路径测试失败: {e}")
        return False
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✓ 健康检查测试通过")
    except Exception as e:
        print(f"✗ 健康检查测试失败: {e}")
        return False
    
    return True

def test_learning_api():
    """测试学习进度API"""
    base_url = "http://localhost:8000/api/v1"
    
    print("\n测试学习进度API...")
    
    # 创建内容
    content_data = {
        "title": "API测试内容",
        "url": "https://example.com/apitest.mp4",
        "duration": 1200,
        "category": "test",
        "reward_points_per_minute": 5,
        "status": True
    }
    
    try:
        response = requests.post(f"{base_url}/contents/contents/", json=content_data)
        assert response.status_code == 200
        content = response.json()
        content_id = content["id"]
        print(f"✓ 内容创建测试通过，ID: {content_id}")
    except Exception as e:
        print(f"✗ 内容创建测试失败: {e}")
        return False
    
    # 开始学习
    try:
        response = requests.post(f"{base_url}/learning/learning/start-learning?content_id={content_id}")
        assert response.status_code == 200
        start_data = response.json()
        session_id = start_data["session_id"]
        print(f"✓ 开始学习测试通过，Session ID: {session_id[:12]}...")
    except Exception as e:
        print(f"✗ 开始学习测试失败: {e}")
        return False
    
    # 更新进度
    try:
        response = requests.post(f"{base_url}/learning/learning/update-progress?session_id={session_id}&watched_duration=300")
        assert response.status_code == 200
        update_data = response.json()
        assert update_data["watched_duration"] == 300
        print("✓ 更新进度测试通过")
    except Exception as e:
        print(f"✗ 更新进度测试失败: {e}")
        return False
    
    # 完成学习
    try:
        response = requests.post(f"{base_url}/learning/learning/complete-learning?session_id={session_id}")
        assert response.status_code == 200
        complete_data = response.json()
        assert "points_earned" in complete_data
        print("✓ 完成学习测试通过")
    except Exception as e:
        print(f"✗ 完成学习测试失败: {e}")
        return False
    
    # 获取用户进度
    try:
        response = requests.get(f"{base_url}/learning/learning/user-progress")
        assert response.status_code == 200
        progress_data = response.json()
        assert isinstance(progress_data, list)
        print("✓ 获取用户进度测试通过")
    except Exception as e:
        print(f"✗ 获取用户进度测试失败: {e}")
        return False
    
    return True

def test_content_api():
    """测试内容管理API"""
    base_url = "http://localhost:8000/api/v1"
    
    print("\n测试内容管理API...")
    
    # 创建内容
    content_data = {
        "title": "功能测试内容",
        "url": "https://example.com/featuretest.mp4",
        "duration": 1800,
        "category": "feature_test",
        "reward_points_per_minute": 3,
        "status": True
    }
    
    try:
        response = requests.post(f"{base_url}/contents/contents/", json=content_data)
        assert response.status_code == 200
        content = response.json()
        content_id = content["id"]
        print(f"✓ 内容创建测试通过，ID: {content_id}")
    except Exception as e:
        print(f"✗ 内容创建测试失败: {e}")
        return False
    
    # 获取内容列表
    try:
        response = requests.get(f"{base_url}/contents/contents/")
        assert response.status_code == 200
        contents = response.json()
        assert isinstance(contents, list)
        print("✓ 获取内容列表测试通过")
    except Exception as e:
        print(f"✗ 获取内容列表测试失败: {e}")
        return False
    
    # 获取单个内容
    try:
        response = requests.get(f"{base_url}/contents/contents/{content_id}")
        assert response.status_code == 200
        content = response.json()
        assert content["id"] == content_id
        print("✓ 获取单个内容测试通过")
    except Exception as e:
        print(f"✗ 获取单个内容测试失败: {e}")
        return False
    
    # 更新内容
    update_data = {
        "title": "已更新的测试内容",
        "category": "updated_test"
    }
    
    try:
        response = requests.put(f"{base_url}/contents/contents/{content_id}", json=update_data)
        assert response.status_code == 200
        updated_content = response.json()
        assert updated_content["title"] == "已更新的测试内容"
        print("✓ 更新内容测试通过")
    except Exception as e:
        print(f"✗ 更新内容测试失败: {e}")
        return False
    
    return True

def test_points_api():
    """测试积分管理API"""
    base_url = "http://localhost:8000/api/v1"
    
    print("\n测试积分管理API...")
    
    # 获取用户积分账户
    try:
        response = requests.get(f"{base_url}/points/points/account")
        assert response.status_code == 200
        account = response.json()
        assert "user_id" in account
        print("✓ 获取积分账户测试通过")
    except Exception as e:
        print(f"✗ 获取积分账户测试失败: {e}")
        return False
    
    # 获取积分流水
    try:
        response = requests.get(f"{base_url}/points/points/transactions")
        assert response.status_code == 200
        transactions = response.json()
        assert isinstance(transactions, list)
        print("✓ 获取积分流水测试通过")
    except Exception as e:
        print(f"✗ 获取积分流水测试失败: {e}")
        return False
    
    return True

def main():
    """主测试函数"""
    print("=" * 50)
    print("开始运行API端到端测试...")
    print("=" * 50)
    
    all_passed = True
    
    # 运行各项测试
    all_passed &= test_api_endpoints()
    all_passed &= test_learning_api()
    all_passed &= test_content_api()
    all_passed &= test_points_api()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有API端到端测试通过！")
    else:
        print("❌ 部分测试失败")
    print("=" * 50)
    
    return all_passed

if __name__ == "__main__":
    main()