#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ting 学习平台 - 带认证的全面测试脚本
"""

import requests
import time
from datetime import datetime

# 基础配置
BASE_URL = "http://www.joyogo.com/tingapi"
BASE_API_URL = "http://www.joyogo.com/tingapi/api/v1"
MOBILE_URL = "http://www.joyogo.com/ting"

# 测试结果统计
test_results = {"passed": 0, "failed": 0, "total": 0}

def log_test(name, status, message=""):
    test_results["total"] += 1
    if status == "PASS":
        test_results["passed"] += 1
        print(f"✅ [PASS] {name}")
    else:
        test_results["failed"] += 1
        print(f"❌ [FAIL] {name}: {message}")

def get_auth_token():
    """获取认证 token"""
    try:
        # 先注册新用户
        test_user = {
            "username": f"test_user_{int(time.time())}",
            "password": "Test123456",
            "phone": f"138{int(time.time()) % 10000:04d}0000"
        }
        
        response = requests.post(
            f"{BASE_API_URL}/auth/auth/register",
            json=test_user,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            log_test("用户注册", "PASS", f"用户 ID: {data['user_id']}")
            return data["token"]
        else:
            log_test("用户注册", "FAIL", f"HTTP {response.status_code}")
            return None
    except Exception as e:
        log_test("用户注册", "FAIL", str(e))
        return None

def test_sign_info(token):
    """测试获取签到信息"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_API_URL}/sign/sign-info", headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if "today_signed" in data:
                log_test("获取签到信息", "PASS", f"今日已签到：{data['today_signed']}")
            else:
                log_test("获取签到信息", "FAIL", "缺少 today_signed 字段")
        else:
            log_test("获取签到信息", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("获取签到信息", "FAIL", str(e))

def test_get_notifications(token):
    """测试获取通知列表"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_API_URL}/sign/notifications", headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                log_test("获取通知列表", "PASS", f"({len(data)} 条通知)")
            else:
                log_test("获取通知列表", "PASS", "返回数据")
        else:
            log_test("获取通知列表", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("获取通知列表", "FAIL", str(e))

def test_analytics_summary(token):
    """测试获取数据分析摘要"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_API_URL}/analytics/analytics/summary", headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if "user_id" in data:
                log_test("获取数据分析摘要", "PASS")
            else:
                log_test("获取数据分析摘要", "FAIL", "缺少 user_id 字段")
        else:
            log_test("获取数据分析摘要", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("获取数据分析摘要", "FAIL", str(e))

def test_conversion_funnel(token):
    """测试获取转化漏斗"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_API_URL}/analytics/analytics/conversion-funnel", headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if "total_users" in data:
                log_test("获取转化漏斗", "PASS", f"总用户：{data['total_users']}")
            else:
                log_test("获取转化漏斗", "FAIL", "缺少 total_users 字段")
        else:
            log_test("获取转化漏斗", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("获取转化漏斗", "FAIL", str(e))

def run_auth_tests():
    """运行需要认证的测试"""
    print("=" * 60)
    print("🧪 Ting 学习平台 - 带认证的全面测试验证")
    print("=" * 60)
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # 获取认证 token
    print("🔐 获取认证 Token")
    print("-" * 60)
    token = get_auth_token()
    
    if not token:
        print("❌ 无法获取认证 token，跳过需要认证的测试")
        return
    
    print()
    
    # 需要认证的测试
    print("🎯 需要认证的功能测试")
    print("-" * 60)
    test_sign_info(token)
    test_get_notifications(token)
    test_analytics_summary(token)
    test_conversion_funnel(token)
    print()
    
    # 测试结果统计
    print("=" * 60)
    print("📈 测试结果统计")
    print("=" * 60)
    print(f"✅ 通过：{test_results['passed']}")
    print(f"❌ 失败：{test_results['failed']}")
    print(f"📝 总计：{test_results['total']}")
    if test_results['total'] > 0:
        print(f"📊 通过率：{test_results['passed'] / test_results['total'] * 100:.1f}%")
    print("=" * 60)
    print(f"⏰ 结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    return test_results["failed"] == 0

if __name__ == "__main__":
    success = run_auth_tests()
    exit(0 if success else 1)
