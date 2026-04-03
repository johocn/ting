"""
验证学习进度功能完整测试
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_full_learning_flow():
    print("=== 完整学习流程测试 ===\n")
    
    # 1. 创建内容
    print("1. 创建学习内容...")
    content_data = {
        "title": "Python编程入门课程",
        "url": "https://example.com/python-course.mp4",
        "duration": 2400,  # 40分钟
        "category": "programming",
        "reward_points_per_minute": 5,
        "status": True
    }
    response = requests.post(f"{BASE_URL}/contents/contents/", json=content_data)
    if response.status_code == 200:
        content = response.json()
        content_id = content['id']
        print(f"   ✓ 内容创建成功，ID: {content_id}")
    else:
        print(f"   ✗ 内容创建失败: {response.status_code}")
        return
    
    # 2. 开始学习
    print("\n2. 开始学习...")
    response = requests.post(f"{BASE_URL}/learning/learning/start-learning?content_id={content_id}")
    if response.status_code == 200:
        start_result = response.json()
        session_id = start_result['session_id']
        print(f"   ✓ 学习会话开始，Session ID: {session_id[:12]}...")
    else:
        print(f"   ✗ 开始学习失败: {response.status_code}")
        return
    
    # 3. 更新学习进度
    print("\n3. 更新学习进度...")
    response = requests.post(f"{BASE_URL}/learning/learning/update-progress?session_id={session_id}&watched_duration=600")
    if response.status_code == 200:
        update_result = response.json()
        print(f"   ✓ 进度更新成功，已学习: {update_result['watched_duration']}秒 ({update_result['progress_percentage']}%)")
    else:
        print(f"   ✗ 更新进度失败: {response.status_code}")
        return
    
    # 4. 再次更新进度
    print("\n4. 继续学习并更新进度...")
    response = requests.post(f"{BASE_URL}/learning/learning/update-progress?session_id={session_id}&watched_duration=1200")
    if response.status_code == 200:
        update_result = response.json()
        print(f"   ✓ 进度更新成功，已学习: {update_result['watched_duration']}秒 ({update_result['progress_percentage']}%)")
    else:
        print(f"   ✗ 更新进度失败: {response.status_code}")
        return
    
    # 5. 完成学习
    print("\n5. 完成学习...")
    response = requests.post(f"{BASE_URL}/learning/learning/complete-learning?session_id={session_id}")
    if response.status_code == 200:
        complete_result = response.json()
        print(f"   ✓ 学习完成")
        print(f"   ✓ 获得积分: {complete_result.get('points_earned', 'N/A')}")
        print(f"   ✓ 总积分: {complete_result.get('total_points', 'N/A')}")
    else:
        print(f"   ✗ 完成学习失败: {response.status_code}")
        print(f"   响应: {response.text}")
        return
    
    # 6. 获取用户学习进度
    print("\n6. 获取用户学习进度...")
    response = requests.get(f"{BASE_URL}/learning/learning/user-progress")
    if response.status_code == 200:
        progress_list = response.json()
        print(f"   ✓ 获取到 {len(progress_list)} 条学习记录")
        for progress in progress_list:
            if progress['session_id'] == session_id:
                print(f"   ✓ 会话: {progress['session_id'][:12]}...")
                print(f"   ✓ 内容: {progress['content']['title']}")
                print(f"   ✓ 状态: {progress['status']}")
                print(f"   ✓ 进度: {progress['progress_percentage']}%")
                break
    else:
        print(f"   ✗ 获取进度失败: {response.status_code}")
        return
    
    # 7. 获取内容学习统计
    print("\n7. 获取内容学习统计...")
    response = requests.get(f"{BASE_URL}/learning/learning/content-progress/{content_id}")
    if response.status_code == 200:
        stats = response.json()
        print(f"   ✓ 内容: {stats['title']}")
        print(f"   ✓ 学习人数: {stats['total_learners']}")
        print(f"   ✓ 完成率: {stats['completion_rate']}%")
        print(f"   ✓ 发放积分: {stats['total_points_distributed']}")
    else:
        print(f"   ✗ 获取统计失败: {response.status_code}")
        return
    
    print("\n=== 测试完成，所有功能正常工作 ===")

if __name__ == "__main__":
    test_full_learning_flow()