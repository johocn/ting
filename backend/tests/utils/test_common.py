import pytest
from datetime import datetime, timedelta
from app.utils.common import (
    format_duration, 
    validate_phone, 
    validate_email, 
    generate_id,
    format_large_number
)

class TestUtils:
    """工具函数测试"""
    
    def test_format_duration(self):
        """测试时长格式化"""
        # 测试秒数
        assert format_duration(0) == "0s"
        assert format_duration(30) == "30s"
        assert format_duration(90) == "1m 30s"
        assert format_duration(3661) == "1h 1m 1s"
        
        # 测试无效输入
        assert format_duration(None) == "0s"
        assert format_duration("invalid") == "0s"
    
    def test_validate_phone(self):
        """测试手机号验证"""
        # 有效手机号
        assert validate_phone("13812345678") == True
        assert validate_phone("15912345678") == True
        assert validate_phone("18812345678") == True
        
        # 无效手机号
        assert validate_phone("12345678901") == False  # 不符合规则
        assert validate_phone("1381234567") == False   # 位数不够
        assert validate_phone("138123456789") == False # 位数过多
        assert validate_phone("") == False
        assert validate_phone("abc12345678") == False
    
    def test_validate_email(self):
        """测试邮箱验证"""
        # 有效邮箱
        assert validate_email("test@example.com") == True
        assert validate_email("user.name@test.org") == True
        assert validate_email("user+tag@example.co.uk") == True
        
        # 无效邮箱
        assert validate_email("invalid-email") == False
        assert validate_email("@example.com") == False
        assert validate_email("test@") == False
        assert validate_email("") == False
    
    def test_generate_id(self):
        """测试ID生成"""
        id1 = generate_id()
        id2 = generate_id()
        
        # ID应该是唯一的
        assert id1 != id2
        
        # ID应该包含前缀（如果没有指定前缀）
        assert isinstance(id1, str)
        assert len(id1) > 0
    
    def test_generate_id_with_prefix(self):
        """测试带前缀的ID生成"""
        id_with_prefix = generate_id("TEST_")
        
        assert id_with_prefix.startswith("TEST_")
        assert len(id_with_prefix) > len("TEST_")
    
    def test_format_large_number(self):
        """测试大数字格式化"""
        assert format_large_number(500) == "500"
        assert format_large_number(1500) == "1.5k"
        assert format_large_number(1500000) == "1.5m"
        assert format_large_number(0) == "0"
        assert format_large_number(None) == ""
        assert format_large_number("") == ""
    
    def test_format_large_number_edge_cases(self):
        """测试大数字格式化边界情况"""
        assert format_large_number(999) == "999"
        assert format_large_number(1000) == "1.0k"
        assert format_large_number(999999) == "1000.0k"  # 实际会显示为1000.0k
        assert format_large_number(1000000) == "1.0m"
