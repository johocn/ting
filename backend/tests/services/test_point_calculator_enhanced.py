"""
积分计算器服务测试
"""
import pytest
from app.services.point_calculator import (
    calculate_watch_video_points,
    calculate_answer_quiz_points,
    calculate_referral_points,
    calculate_daily_checkin_points
)

def test_calculate_watch_video_points():
    """测试观看视频积分计算"""
    # 测试基本情况：10分钟，每分钟5分
    points = calculate_watch_video_points(
        duration_seconds=600,  # 10分钟
        rate_per_minute=5
    )
    assert points == 50  # 10 * 5 = 50
    
    # 测试带完整观看奖励的情况
    points_with_bonus = calculate_watch_video_points(
        duration_seconds=1200,  # 20分钟
        rate_per_minute=3,
        full_completion_bonus=20
    )
    assert points_with_bonus == 80  # 20 * 3 + 20 = 80
    
    # 测试零或负数时返回0
    zero_points = calculate_watch_video_points(
        duration_seconds=0,
        rate_per_minute=5
    )
    assert zero_points == 0
    
    negative_points = calculate_watch_video_points(
        duration_seconds=-100,
        rate_per_minute=5
    )
    assert negative_points == 0
    
    # 测试小数分钟情况
    decimal_points = calculate_watch_video_points(
        duration_seconds=90,  # 1.5分钟
        rate_per_minute=10
    )
    assert decimal_points == 15  # int(1.5 * 10) = 15

def test_calculate_answer_quiz_points():
    """测试答题积分计算"""
    # 测试基本情况：8题对8题，每题10分
    points = calculate_answer_quiz_points(
        correct_answers=8,
        total_questions=10,
        points_per_question=10
    )
    assert points == 80  # 8 * 10 = 80
    
    # 测试全部答对带奖励
    perfect_points = calculate_answer_quiz_points(
        correct_answers=10,
        total_questions=10,
        points_per_question=5,
        completion_bonus=30
    )
    assert perfect_points == 80  # 10 * 5 + 30 = 80
    
    # 测试零题或错误输入
    zero_points = calculate_answer_quiz_points(
        correct_answers=0,
        total_questions=10,
        points_per_question=10
    )
    assert zero_points == 0
    
    zero_total = calculate_answer_quiz_points(
        correct_answers=5,
        total_questions=0,
        points_per_question=10
    )
    assert zero_total == 0
    
    negative_points = calculate_answer_quiz_points(
        correct_answers=-1,
        total_questions=10,
        points_per_question=10
    )
    assert negative_points == 0

def test_calculate_referral_points():
    """测试推荐积分计算"""
    # 测试基本情况
    points = calculate_referral_points(
        referral_type="registration",
        base_reward=100,
        level_multiplier=1.5
    )
    assert points == 150  # 100 * 1.5 = 150
    
    # 测试默认倍数
    default_points = calculate_referral_points(
        referral_type="purchase",
        base_reward=50
    )
    assert default_points == 50  # 50 * 1.0 = 50
    
    # 测试不同倍数
    low_multiplier_points = calculate_referral_points(
        referral_type="sharing",
        base_reward=200,
        level_multiplier=0.5
    )
    assert low_multiplier_points == 100  # 200 * 0.5 = 100

def test_calculate_daily_checkin_points():
    """测试每日签到积分计算"""
    # 测试基础签到
    base_points = calculate_daily_checkin_points(
        consecutive_days=1,
        base_points=10
    )
    assert base_points == 10  # 基础积分
    
    # 测试7天签到奖励
    seven_day_points = calculate_daily_checkin_points(
        consecutive_days=7,
        base_points=10
    )
    assert seven_day_points == 15  # 10 + 5 = 15
    
    # 测试14天签到奖励
    fourteen_day_points = calculate_daily_checkin_points(
        consecutive_days=14,
        base_points=10
    )
    assert fourteen_day_points == 20  # 10 + 5 + 5 = 20
    
    # 测试30天签到奖励
    thirty_day_points = calculate_daily_checkin_points(
        consecutive_days=30,
        base_points=10
    )
    assert thirty_day_points == 30  # 10 + 5 + 5 + 10 = 30
    
    # 测试更长连续签到
    long_streak_points = calculate_daily_checkin_points(
        consecutive_days=45,
        base_points=5
    )
    assert long_streak_points == 15  # 5 + 5 + 5 = 15 (只计算最高奖励)

def test_edge_cases():
    """测试边界情况"""
    # 非常大的数值
    large_points = calculate_watch_video_points(
        duration_seconds=36000,  # 10小时
        rate_per_minute=10
    )
    assert large_points == 6000  # 600 * 10 = 6000
    
    # 非常小的数值
    small_points = calculate_watch_video_points(
        duration_seconds=30,  # 0.5分钟
        rate_per_minute=10
    )
    assert small_points == 5  # int(0.5 * 10) = 5
    
    # 非整数分钟
    fractional_points = calculate_watch_video_points(
        duration_seconds=150,  # 2.5分钟
        rate_per_minute=8
    )
    assert fractional_points == 20  # int(2.5 * 8) = 20

if __name__ == "__main__":
    # 运行测试
    test_calculate_watch_video_points()
    test_calculate_answer_quiz_points()
    test_calculate_referral_points()
    test_calculate_daily_checkin_points()
    test_edge_cases()
    print("所有积分计算器测试通过！")