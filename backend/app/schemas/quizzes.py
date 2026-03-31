from pydantic import BaseModel
from typing import List, Union

class QuestionAnswer(BaseModel):
    question_id: int
    user_answer: Union[str, List[str]]  # 单选题用str，多选题用List[str]

class QuizSubmission(BaseModel):
    content_id: int
    answers: List[QuestionAnswer]

class QuizConfigUpdate(BaseModel):
    total_questions: int
    required_correct: int
    pass_percentage: float
    quiz_points: int
    time_limit: int
    allow_retry: bool
    retry_limit: int

class QuizResult(BaseModel):
    passed: bool
    score: float
    correct_count: int
    total_questions: int
    earned_points: int
    message: str
    responses: List[dict]

class QuestionCreate(BaseModel):
    question_text: str
    options: dict
    correct_answer: str
    individual_points: int = 20
    question_order: int = 0

class QuestionUpdate(BaseModel):
    question_text: str
    options: dict
    correct_answer: str
    individual_points: int
    question_order: int
