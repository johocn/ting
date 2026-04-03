"""
积分计算器服务测试（无pytest依赖）
"""
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
    assert points == 50, f"期望50分，实际{points}分"
    print("✓ 观看视频积分计算测试通过")
    
    # 测试带完整观看奖励的情况
    points_with_bonus = calculate_watch_video_points(
        duration_seconds=1200,  # 20分钟
        rate_per_minute=3,
        full_completion_bonus=20
    )
    assert points_with_bonus == 80, f"期望80分，实际{points_with_bonus}分"
    print("✓ 带奖励的视频积分计算测试通过")
    
    # 测试零或负数时返回0
    zero_points = calculate_watch_video_points(
        duration_seconds=0,
        rate_per_minute=5
    )
    assert zero_points == 0, f"期望0分，实际{zero_points}分"
    print("✓ 零时长积分计算测试通过")
    
    negative_points = calculate_watch_video_points(
        duration_seconds=-100,
        rate_per_minute=5
    )
    assert negative_points == 0, f"期望0分，实际{zero_points}分"
    print("✓ 负时长积分计算测试通过")
    
    # 测试小数分钟情况
    decimal_points = calculate_watch_video_points(
        duration_seconds=90,  # 1.5分钟
        rate_per_minute=10
    )
    assert decimal_points == 15, f"期望15分，实际{decimal_points}分"
    print("✓ 小数分钟积分计算测试通过")

def test_calculate_answer_quiz_points():
    """测试答题积分计算"""
    # 测试基本情况：8题对8题，每题10分
    points = calculate_answer_quiz_points(
        correct_answers=8,
        total_questions=10,
        points_per_question=10
    )
    assert points == 80, f"期望80分，实际{points}分"
    print("✓ 答题积分计算测试通过")
    
    # 测试全部答对带奖励
    perfect_points = calculate_answer_quiz_points(
        correct_answers=10,
        total_questions=10,
        points_per_question=5,
        completion_bonus=30
    )
    assert perfect_points == 80, f"期望80分，实际{perfect_points}分"
    print("✓ 全部答对带奖励积分计算测试通过")
    
    # 测试零题或错误输入
    zero_points = calculate_answer_quiz_points(
        correct_answers=0,
        total_questions=10,
        points_per_question=10
    )
    assert zero_points == 0, f"期望0分，实际{zero_points}分"
    print("✓ 零正确题数积分计算测试通过")
    
    zero_total = calculate_answer_quiz_points(
        correct_answers=5,
        total_questions=0,
        points_per_question=10
    )
    assert zero_total == 0, f"期望0分，实际{zero_total}分"
    print("✓ 零总题数积分计算测试通过")
    
    negative_points = calculate_answer_quiz_points(
        correct_answers=-1,
        total_questions=10,
        points_per_question=10
    )
    assert negative_points == 0, f"期望0分，实际{negative_points}分"
    print("✓ 负正确题数积分计算测试通过")

def test_calculate_referral_points():
    """测试推荐积分计算"""
    # 测试基本情况
    points = calculate_referral_points(
        referral_type="registration",
        base_reward=100,
        level_multiplier=1.5
    )
    assert points == 150, f"期望150分，实际{points}分"
    print("✓ 推荐积分计算测试通过")
    
    # 测试默认倍数
    default_points = calculate_referral_points(
        referral_type="purchase",
        base_reward=50
    )
    assert default_points == 50, f"期望50分，实际{default_points}分"
    print("✓ 默认倍数推荐积分计算测试通过")
    
    # 测试不同倍数
    low_multiplier_points = calculate_referral_points(
        referral_type="sharing",
        base_reward=200,
        level_multiplier=0.5
    )
    assert low_multiplier_points == 100, f"期望100分，实际{low_multiplier_points}分"
    print("✓ 低倍数推荐积分计算测试通过")

def test_calculate_daily_checkin_points():
    """测试每日签到积分计算"""
    # 测试基础签到
    base_points = calculate_daily_checkin_points(
        consecutive_days=1,
        base_points=10
    )
    assert base_points == 10, f"期望10分，实际{base_points}分"
    print("✓ 基础签到积分计算测试通过")
    
    # 测试7天签到奖励
    seven_day_points = calculate_daily_checkin_points(
        consecutive_days=7,
        base_points=10
    )
    assert seven_day_points == 15, f"期望15分，实际{seven_day_points}分"
    print("✓ 7天签到奖励积分计算测试通过")
    
    # 测试14天签到奖励
    fourteen_day_points = calculate_daily_checkin_points(
        consecutive_days=14,
        base_points=10
    )
    assert fourteen_day_points == 20, f"期望20分，实际{fourteen_day_points}分"
    print("✓ 14天签到奖励积分计算测试通过")
    
    # 测试30天签到奖励
    thirty_day_points = calculate_daily_checkin_points(
        consecutive_days=30,
        base_points=10
    )
    assert thirty_day_points == 30, f"期望30分，实际{thirty_day_points}分"
    print("✓ 30天签到奖励积分计算测试通过")
    
    # 测试更长连续签到
    long_streak_points = calculate_daily_checkin_points(
        consecutive_days=45,
        base_points=5
    )
    assert long_streak_points == 15, f"期望15分，实际{long_streak_points}分"
    print("✓ 长期签到积分计算测试通过")

def test_edge_cases():
    """测试边界情况"""
    # 非常大的数值
    large_points = calculate_watch_video_points(
        duration_seconds=36000,  # 10小时
        rate_per_minute=10
    )
    assert large_points == 6000, f"期望6000分，实际{large_points}分"
    print("✓ 大数值积分计算测试通过")
    
    # 非常小的数值
    small_points = calculate_watch_video_points(
        duration_seconds=30,  # 0.5分钟
        rate_per_minute=10
    )
    assert small_points == 5, f"期望5分，实际{small_points}分"
    print("✓ 小数值积分计算测试通过")
    
    # 非整数分钟
    fractional_points = calculate_watch_video_points(
        duration_seconds=150,  # 2.5分钟
        rate_per_minute=8
    )
    assert fractional_points == 20, f"期望20分，实际{fractional_points}分"
    print("✓ 非整数分钟积分计算测试通过")

if __name__ == "__main__":
    print("开始运行积分计算器服务测试...")
    try:
        test_calculate_watch_video_points()
        test_calculate_answer_quiz_points()
        test_calculate_referral_points()
        test_calculate_daily_checkin_points()
        test_edge_cases()
        print("\n🎉 所有积分计算器测试通过！")
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
    except Exception as e:
        print(f"\n💥 测试过程中发生错误: {e}")