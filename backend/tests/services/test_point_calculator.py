import pytest
from app.services.point_calculator import (
    calculate_watch_video_points,
    calculate_answer_quiz_points,
    calculate_referral_points,
    calculate_daily_checkin_points
)

class TestPointCalculator:
    """积分计算器测试"""
    
    def test_calculate_watch_video_points(self):
        """测试观看视频积分计算"""
        # 正常观看
        points = calculate_watch_video_points(duration_seconds=1800, rate_per_minute=5)  # 30分钟 * 5分/分钟
        assert points == 150
        
        # 部分观看
        points = calculate_watch_video_points(duration_seconds=900, rate_per_minute=5)  # 15分钟 * 5分/分钟
        assert points == 75
        
        # 完整观看奖励
        points = calculate_watch_video_points(
            duration_seconds=1800, 
            rate_per_minute=5, 
            full_completion_bonus=20
        )
        assert points == 170  # 150 + 20
        
        # 边界情况
        points = calculate_watch_video_points(duration_seconds=0, rate_per_minute=5)
        assert points == 0
        
        points = calculate_watch_video_points(duration_seconds=30, rate_per_minute=5)  # 0.5分钟
        assert points == 2  # 向下取整
    
    def test_calculate_answer_quiz_points(self):
        """测试答题积分计算"""
        # 正确回答
        correct_answers = 8
        total_questions = 10
        base_points_per_question = 20
        quiz_completion_bonus = 100
        
        points = calculate_answer_quiz_points(
            correct_answers=correct_answers,
            total_questions=total_questions,
            points_per_question=base_points_per_question,
            completion_bonus=quiz_completion_bonus
        )
        
        expected = (correct_answers * base_points_per_question) + quiz_completion_bonus
        assert points == expected
        
        # 部分正确
        partial_points = calculate_answer_quiz_points(
            correct_answers=5,
            total_questions=10,
            points_per_question=20,
            completion_bonus=100  # 未完成，不应获得奖励
        )
        
        assert partial_points == 100  # 5 * 20
        
        # 全部正确
        full_points = calculate_answer_quiz_points(
            correct_answers=10,
            total_questions=10,
            points_per_question=20,
            completion_bonus=100
        )
        
        assert full_points == 300  # 10 * 20 + 100
    
    def test_calculate_referral_points(self):
        """测试推荐积分计算"""
        # 基础推荐奖励
        points = calculate_referral_points(referral_type="register", base_reward=50)
        assert points == 50
        
        # 高级推荐奖励
        points = calculate_referral_points(referral_type="first_purchase", base_reward=100)
        assert points == 100
        
        # 层级奖励
        points = calculate_referral_points(
            referral_type="register",
            base_reward=50,
            level_multiplier=1.5
        )
        assert points == 75  # 50 * 1.5
    
    def test_calculate_daily_checkin_points(self):
        """测试每日签到积分计算"""
        # 连续签到奖励
        consecutive_days = 1
        base_points = 5
        bonus_points = 0
        
        points = calculate_daily_checkin_points(consecutive_days=consecutive_days, base_points=base_points)
        assert points == 5
        
        # 连续签到奖励
        consecutive_days = 7
        points = calculate_daily_checkin_points(consecutive_days=consecutive_days, base_points=base_points)
        # 7天签到可能有额外奖励
        assert points >= 5
        
        # 连续签到奖励递增
        consecutive_days = 30
        points = calculate_daily_checkin_points(consecutive_days=consecutive_days, base_points=base_points)
        # 30天签到可能有更多奖励
        assert points >= 5
