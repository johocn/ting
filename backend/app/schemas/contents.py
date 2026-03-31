from pydantic import BaseModel
from typing import Optional, Dict, Any

class ContentBase(BaseModel):
    title: str
    url: str
    duration: Optional[int] = 0
    category: Optional[str] = ""
    reward_points_per_minute: Optional[int] = 5
    status: Optional[bool] = True

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    duration: Optional[int] = None
    category: Optional[str] = None
    reward_points_per_minute: Optional[int] = None
    status: Optional[bool] = None

class QuestionBase(BaseModel):
    question_text: str
    options: Dict[str, str]  # 选项字典，如 {"A": "选项A", "B": "选项B"}
    correct_answer: str  # 正确答案，如 "A"
    individual_points: Optional[int] = 20
    question_order: Optional[int] = 0

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    options: Optional[Dict[str, str]] = None
    correct_answer: Optional[str] = None
    individual_points: Optional[int] = None
    question_order: Optional[int] = None

class ContentQuizConfigBase(BaseModel):
    total_questions: Optional[int] = 10
    required_correct: Optional[int] = 8
    pass_percentage: Optional[int] = 80
    quiz_points: Optional[int] = 100
    time_limit: Optional[int] = None
    allow_retry: Optional[bool] = False
    retry_limit: Optional[int] = 1

class ContentQuizConfigCreate(ContentQuizConfigBase):
    content_id: int

class ContentQuizConfigUpdate(BaseModel):
    total_questions: Optional[int] = None
    required_correct: Optional[int] = None
    pass_percentage: Optional[int] = None
    quiz_points: Optional[int] = None
    time_limit: Optional[int] = None
    allow_retry: Optional[bool] = None
    retry_limit: Optional[int] = None
