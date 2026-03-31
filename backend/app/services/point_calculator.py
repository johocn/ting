"""
积分计算器服务
"""

def calculate_watch_video_points(
    duration_seconds: int, 
    rate_per_minute: float,
    full_completion_bonus: int = 0
) -> int:
    """
    计算观看视频积分
    
    Args:
        duration_seconds: 观看时长（秒）
        rate_per_minute: 每分钟获得积分
        full_completion_bonus: 完整观看奖励积分
    
    Returns:
        计算得到的积分
    """
    if duration_seconds <= 0:
        return 0
    
    minutes = duration_seconds / 60
    base_points = int(minutes * rate_per_minute)
    
    # 如果完整观看，给予额外奖励
    if full_completion_bonus > 0:
        base_points += full_completion_bonus
    
    return base_points

def calculate_answer_quiz_points(
    correct_answers: int,
    total_questions: int,
    points_per_question: int,
    completion_bonus: int = 0
) -> int:
    """
    计算答题积分
    
    Args:
        correct_answers: 正确题数
        total_questions: 总题数
        points_per_question: 每题积分
        completion_bonus: 完成奖励积分
    
    Returns:
        计算得到的积分
    """
    if correct_answers <= 0 or total_questions <= 0:
        return 0
    
    base_points = correct_answers * points_per_question
    
    # 如果全部答对，给予额外奖励
    if correct_answers == total_questions and completion_bonus > 0:
        base_points += completion_bonus
    
    return base_points

def calculate_referral_points(
    referral_type: str,
    base_reward: int,
    level_multiplier: float = 1.0
) -> int:
    """
    计算推荐积分
    
    Args:
        referral_type: 推荐类型
        base_reward: 基础奖励积分
        level_multiplier: 层级倍数
    
    Returns:
        计算得到的积分
    """
    return int(base_reward * level_multiplier)

def calculate_daily_checkin_points(
    consecutive_days: int,
    base_points: int
) -> int:
    """
    计算每日签到积分
    
    Args:
        consecutive_days: 连续签到天数
        base_points: 基础积分
    
    Returns:
        计算得到的积分
    """
    # 基础积分
    points = base_points
    
    # 连续签到奖励
    if consecutive_days >= 7:
        points += 5  # 7天签到额外奖励
    if consecutive_days >= 14:
        points += 10  # 14天签到额外奖励
    if consecutive_days >= 30:
        points += 20  # 30天签到额外奖励
    
    return points
