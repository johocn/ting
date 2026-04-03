from pydantic import BaseModel
from typing import Optional, List

class LearningProgressCreate(BaseModel):
    """创建学习进度"""
    user_id: int
    content_id: int
    session_id: str
    watched_duration: int = 0
    status: str = "in_progress"

class LearningProgressUpdate(BaseModel):
    """更新学习进度"""
    watched_duration: Optional[int] = None
    status: Optional[str] = None

class LearningSessionStartResponse(BaseModel):
    """开始学习会话响应"""
    session_id: str
    message: str
    start_time: str
    content: dict

class LearningProgressUpdateResponse(BaseModel):
    """更新学习进度响应"""
    session_id: str
    watched_duration: int
    total_duration: int
    progress_percentage: float
    message: str

class LearningCompleteResponse(BaseModel):
    """完成学习响应"""
    session_id: str
    watched_duration: int
    points_earned: int
    total_points: int
    message: str

class UserLearningProgressResponse(BaseModel):
    """用户学习进度响应"""
    session_id: str
    content: dict
    watched_duration: int
    progress_percentage: float
    status: str
    start_time: Optional[str]
    completed_at: Optional[str]

class ContentLearningStatsResponse(BaseModel):
    """内容学习统计响应"""
    content_id: int
    title: str
    total_learners: int
    completion_rate: float
    average_duration: int
    total_points_distributed: int