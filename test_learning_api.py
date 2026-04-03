"""
测试新添加的学习进度API功能
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_learning_api():
    print("开始测试学习进度API...")
    
    # 首先尝试获取内容列表
    print("\n1. 获取内容列表...")
    try:
        response = requests.get(f"{BASE_URL}/contents/contents/")
        print(f"内容API响应: {response.status_code}")
        if response.status_code == 200:
            contents = response.json()
            print(f"获取到 {len(contents)} 个内容")
            if contents:
                content_id = contents[0]['id'] if len(contents) > 0 else None
            else:
                print("没有找到任何内容，将创建一个测试内容")
                content_id = create_test_content()
        else:
            print("获取内容失败，尝试创建测试内容")
            content_id = create_test_content()
    except Exception as e:
        print(f"获取内容时出错: {e}")
        content_id = create_test_content()
    
    if content_id:
        print(f"\n2. 开始学习内容 (ID: {content_id})...")
        start_response = start_learning(content_id)
        if start_response and 'session_id' in start_response:
            session_id = start_response['session_id']
            print(f"学习会话已创建: {session_id}")
            
            print("\n3. 更新学习进度...")
            update_response = update_progress(session_id, 300)  # 假设学习了5分钟
            if update_response:
                print("学习进度更新成功")
                
                print("\n4. 完成学习...")
                complete_response = complete_learning(session_id)
                if complete_response:
                    print("学习完成，积分已发放")
                    
                    print("\n5. 获取用户学习进度...")
                    progress_response = get_user_progress()
                    if progress_response:
                        print("成功获取用户学习进度")
                        print(f"学习记录数: {len(progress_response)}")
                        
                        for progress in progress_response:
                            print(f"- 会话: {progress['session_id'][:8]}..., "
                                  f"内容: {progress['content']['title']}, "
                                  f"进度: {progress['progress_percentage']}%")
    
    print("\n测试完成!")

def create_test_content():
    """创建测试内容"""
    try:
        content_data = {
            "title": "测试视频课程",
            "url": "https://example.com/video.mp4",
            "duration": 1800,  # 30分钟
            "category": "education",
            "reward_points_per_minute": 5,
            "status": True
        }
        response = requests.post(f"{BASE_URL}/contents/contents/", json=content_data)
        if response.status_code == 200:
            result = response.json()
            print(f"测试内容创建成功，ID: {result['id']}")
            return result['id']
        else:
            print(f"创建测试内容失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"创建测试内容时出错: {e}")
        return None

def start_learning(content_id):
    """开始学习"""
    try:
        response = requests.post(f"{BASE_URL}/learning/learning/start-learning?content_id={content_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"开始学习失败: {response.status_code}")
            print(f"响应: {response.text}")
            return None
    except Exception as e:
        print(f"开始学习时出错: {e}")
        return None

def update_progress(session_id, duration):
    """更新学习进度"""
    try:
        response = requests.post(f"{BASE_URL}/learning/learning/update-progress?session_id={session_id}&watched_duration={duration}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"更新进度失败: {response.status_code}")
            print(f"响应: {response.text}")
            return None
    except Exception as e:
        print(f"更新进度时出错: {e}")
        return None

def complete_learning(session_id):
    """完成学习"""
    try:
        response = requests.post(f"{BASE_URL}/learning/learning/complete-learning?session_id={session_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"完成学习失败: {response.status_code}")
            print(f"响应: {response.text}")
            return None
    except Exception as e:
        print(f"完成学习时出错: {e}")
        return None

def get_user_progress():
    """获取用户学习进度"""
    try:
        response = requests.get(f"{BASE_URL}/learning/learning/user-progress")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"获取进度失败: {response.status_code}")
            print(f"响应: {response.text}")
            return None
    except Exception as e:
        print(f"获取进度时出错: {e}")
        return None

if __name__ == "__main__":
    test_learning_api()