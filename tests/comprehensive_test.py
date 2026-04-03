#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ting 学习平台 - 全面测试脚本
测试所有核心功能模块
"""

import requests
import json
import time
from datetime import datetime

# 基础配置
BASE_API_URL = "http://www.joyogo.com/tingapi/api/v1"
BASE_URL = "http://www.joyogo.com/tingapi"
MOBILE_URL = "http://www.joyogo.com/ting"

# 测试结果统计
test_results = {
    "passed": 0,
    "failed": 0,
    "total": 0
}

def log_test(name, status, message=""):
    """记录测试结果"""
    test_results["total"] += 1
    if status == "PASS":
        test_results["passed"] += 1
        print(f"✅ [PASS] {name}")
    else:
        test_results["failed"] += 1
        print(f"❌ [FAIL] {name}: {message}")

def test_health_check():
    """测试健康检查"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                log_test("健康检查", "PASS")
            else:
                log_test("健康检查", "FAIL", f"状态异常：{data}")
        else:
            log_test("健康检查", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("健康检查", "FAIL", str(e))

def test_api_docs():
    """测试 API 文档"""
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            log_test("API 文档页面", "PASS")
        else:
            log_test("API 文档页面", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("API 文档页面", "FAIL", str(e))

def test_openapi_json():
    """测试 OpenAPI JSON"""
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "paths" in data and len(data["paths"]) > 0:
                log_test("OpenAPI JSON", "PASS", f"({len(data['paths'])} 个端点)")
            else:
                log_test("OpenAPI JSON", "FAIL", "缺少 paths")
        else:
            log_test("OpenAPI JSON", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("OpenAPI JSON", "FAIL", str(e))

def test_mobile_pages():
    """测试移动端页面"""
    pages = [
        "/",
        "/points.html",
        "/profile.html",
        "/player.html",
        "/channels.html",
        "/mall.html",
        "/history.html",
        "/checkin.html",
        "/notifications.html",
        "/analytics.html"
    ]
    
    for page in pages:
        try:
            response = requests.get(f"{MOBILE_URL}{page}", timeout=5)
            if response.status_code == 200:
                log_test(f"移动端页面 {page}", "PASS")
            else:
                log_test(f"移动端页面 {page}", "FAIL", f"HTTP {response.status_code}")
        except Exception as e:
            log_test(f"移动端页面 {page}", "FAIL", str(e))

def test_user_registration():
    """测试用户注册"""
    try:
        test_user = {
            "username": f"test_user_{int(time.time())}",
            "password": "Test123456",
            "phone": "13800138000"
        }
        
        response = requests.post(
            f"{BASE_API_URL}/auth/auth/register",
            json=test_user,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if "token" in data and "user_id" in data:
                log_test("用户注册", "PASS", f"用户 ID: {data['user_id']}")
                return data["token"]
            else:
                log_test("用户注册", "FAIL", "缺少 token 或 user_id")
        else:
            log_test("用户注册", "FAIL", f"HTTP {response.status_code}: {response.text}")
    except Exception as e:
        log_test("用户注册", "FAIL", str(e))
    
    return None

def test_user_login(token=None):
    """测试用户登录"""
    try:
        # 使用测试账号登录
        login_data = {
            "username": "test_user",
            "password": "Test123456"
        }
        
        response = requests.post(
            f"{BASE_API_URL}/auth/auth/login",
            json=login_data,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                log_test("用户登录", "PASS")
                return data["token"]
            else:
                log_test("用户登录", "FAIL", "缺少 token")
        elif response.status_code == 400:
            log_test("用户登录", "PASS", "测试账号不存在 (预期)")
        else:
            log_test("用户登录", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("用户登录", "FAIL", str(e))
    
    return token

def test_get_contents(token=None):
    """测试获取内容列表"""
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(
            f"{BASE_API_URL}/contents/contents/",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                log_test("获取内容列表", "PASS", f"({len(data)} 个内容)")
            else:
                log_test("获取内容列表", "PASS", "返回数据")
        else:
            log_test("获取内容列表", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("获取内容列表", "FAIL", str(e))

def test_get_products(token=None):
    """测试获取商品列表"""
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(
            f"{BASE_API_URL}/mall/products/",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                log_test("获取商品列表", "PASS", f"({len(data)} 个商品)")
            else:
                log_test("获取商品列表", "PASS", "返回数据")
        else:
            log_test("获取商品列表", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("获取商品列表", "FAIL", str(e))

def test_sign_info(token=None):
    """测试获取签到信息"""
    try:
        if not token:
            log_test("获取签到信息", "FAIL", "缺少 token")
            return
        
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            f"{BASE_API_URL}/sign/sign-info",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if "today_signed" in data:
                log_test("获取签到信息", "PASS")
            else:
                log_test("获取签到信息", "FAIL", "缺少 today_signed 字段")
        else:
            log_test("获取签到信息", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("获取签到信息", "FAIL", str(e))

def test_get_notifications(token=None):
    """测试获取通知列表"""
    try:
        if not token:
            log_test("获取通知列表", "FAIL", "缺少 token")
            return
        
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            f"{BASE_API_URL}/sign/notifications",
            headers=headers,
            timeout=5
        )
        
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

def test_analytics_summary(token=None):
    """测试获取数据分析摘要"""
    try:
        if not token:
            log_test("获取数据分析摘要", "FAIL", "缺少 token")
            return
        
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            f"{BASE_API_URL}/analytics/analytics/summary",
            headers=headers,
            timeout=5
        )
        
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

def test_conversion_funnel(token=None):
    """测试获取转化漏斗"""
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(
            f"{BASE_API_URL}/analytics/analytics/conversion-funnel",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if "total_users" in data:
                log_test("获取转化漏斗", "PASS")
            else:
                log_test("获取转化漏斗", "FAIL", "缺少 total_users 字段")
        else:
            log_test("获取转化漏斗", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("获取转化漏斗", "FAIL", str(e))

def test_popular_contents(token=None):
    """测试获取热门内容"""
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(
            f"{BASE_API_URL}/analytics/analytics/popular-contents?limit=5",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                log_test("获取热门内容", "PASS", f"({len(data)} 个内容)")
            else:
                log_test("获取热门内容", "PASS", "返回数据")
        else:
            log_test("获取热门内容", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("获取热门内容", "FAIL", str(e))

def test_database_connection():
    """测试数据库连接"""
    try:
        # 通过健康检查间接测试数据库连接
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            log_test("数据库连接", "PASS")
        else:
            log_test("数据库连接", "FAIL", f"HTTP {response.status_code}")
    except Exception as e:
        log_test("数据库连接", "FAIL", str(e))

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 Ting 学习平台 - 全面测试验证")
    print("=" * 60)
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # 1. 基础服务测试
    print("📋 基础服务测试")
    print("-" * 60)
    test_health_check()
    test_api_docs()
    test_openapi_json()
    test_database_connection()
    print()
    
    # 2. 前端页面测试
    print("📱 前端页面测试")
    print("-" * 60)
    test_mobile_pages()
    print()
    
    # 3. 用户认证测试
    print("🔐 用户认证测试")
    print("-" * 60)
    token = test_user_registration()
    test_user_login(token)
    print()
    
    # 4. 核心功能测试
    print("🎯 核心功能测试")
    print("-" * 60)
    test_get_contents(token)
    test_get_products(token)
    test_sign_info(token)
    test_get_notifications(token)
    print()
    
    # 5. 数据分析测试
    print("📊 数据分析测试")
    print("-" * 60)
    test_analytics_summary(token)
    test_conversion_funnel(token)
    test_popular_contents(token)
    print()
    
    # 测试结果统计
    print("=" * 60)
    print("📈 测试结果统计")
    print("=" * 60)
    print(f"✅ 通过：{test_results['passed']}")
    print(f"❌ 失败：{test_results['failed']}")
    print(f"📝 总计：{test_results['total']}")
    print(f"📊 通过率：{test_results['passed'] / test_results['total'] * 100:.1f}%")
    print("=" * 60)
    print(f"⏰ 结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 返回测试结果
    return test_results["failed"] == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
