from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.contents import Content, Question, ContentQuizConfig
from app.models.points import UserPointAccount
from app.schemas.quizzes import QuizSubmission

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.get("/{content_id}/questions", response_model=List[dict])
async def get_content_questions(content_id: int, db: Session = Depends(get_db)):
    """获取内容相关的问题"""
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")
    
    questions = db.query(Question).filter(
        Question.content_id == content_id
    ).order_by(Question.question_order).all()
    
    return [{
        "id": q.id,
        "question_text": q.question_text,
        "options": q.options,
        "question_type": "single_choice",  # 默认单选题
        "points": q.individual_points
    } for q in questions]

@router.get("/{content_id}/config", response_model=dict)
async def get_quiz_config(content_id: int, db: Session = Depends(get_db)):
    """获取内容的答题配置"""
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")
    
    config = db.query(ContentQuizConfig).filter(
        ContentQuizConfig.content_id == content_id
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="答题配置不存在")
    
    return {
        "content_id": config.content_id,
        "total_questions": config.total_questions,
        "required_correct": config.required_correct,
        "pass_percentage": config.pass_percentage,
        "quiz_points": config.quiz_points,
        "time_limit": config.time_limit,
        "allow_retry": config.allow_retry,
        "retry_limit": config.retry_limit
    }

@router.post("/submit", response_model=dict)
async def submit_quiz(submission: QuizSubmission, db: Session = Depends(get_db)):
    """提交答题"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 获取内容和配置
    content = db.query(Content).filter(Content.id == submission.content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")
    
    config = db.query(ContentQuizConfig).filter(
        ContentQuizConfig.content_id == submission.content_id
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="答题配置不存在")
    
    # 获取题目
    question_ids = [ans.question_id for ans in submission.answers]
    questions = db.query(Question).filter(
        Question.id.in_(question_ids),
        Question.content_id == submission.content_id
    ).all()
    
    question_map = {q.id: q for q in questions}
    
    # 计算得分
    correct_count = 0
    total_score = 0
    responses = []
    
    for answer in submission.answers:
        question = question_map.get(answer.question_id)
        if not question:
            continue
        
        user_answer = answer.user_answer
        correct_answer = question.correct_answer
        
        # 检查答案是否正确
        is_correct = False
        if isinstance(user_answer, list):
            # 多选题
            correct_answer_parsed = eval(correct_answer) if correct_answer.startswith('[') else correct_answer
            if isinstance(correct_answer_parsed, list):
                is_correct = set(user_answer) == set(correct_answer_parsed)
            else:
                is_correct = str(user_answer) == str(correct_answer_parsed)
        else:
            # 单选题或判断题
            correct_answer_parsed = eval(correct_answer) if correct_answer.startswith('[') else correct_answer
            if isinstance(correct_answer_parsed, list):
                is_correct = str(user_answer) in [str(item) for item in correct_answer_parsed]
            else:
                is_correct = str(user_answer) == str(correct_answer_parsed)
        
        if is_correct:
            correct_count += 1
            total_score += question.individual_points
        
        responses.append({
            "question_id": question.id,
            "user_answer": user_answer,
            "is_correct": is_correct,
            "points_earned": question.individual_points if is_correct else 0
        })
    
    # 计算总分和通过状态
    total_questions = len(questions)
    score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    passed = score_percentage >= config.pass_percentage
    
    # 计算并发放积分
    earned_points = 0
    if passed:
        earned_points = config.quiz_points  # 答题奖励积分
    
    # 添加单题积分
    earned_points += sum(r["points_earned"] for r in responses)
    
    # 更新用户积分
    user_account = db.query(UserPointAccount).filter(
        UserPointAccount.user_id == user_id
    ).first()
    
    if not user_account:
        user_account = UserPointAccount(user_id=user_id)
        db.add(user_account)
    
    user_account.available_points += earned_points
    user_account.total_points += earned_points
    
    db.commit()
    
    return {
        "passed": passed,
        "score": round(score_percentage, 2),
        "correct_count": correct_count,
        "total_questions": total_questions,
        "earned_points": earned_points,
        "message": "答题提交成功" if passed else "答题未通过",
        "responses": responses
    }

@router.get("/{content_id}/user-progress", response_model=dict)
async def get_user_quiz_progress(content_id: int, db: Session = Depends(get_db)):
    """获取用户答题进度"""
    user_id = 1  # 实际应用中应从认证信息获取
    
    # 检查用户是否已完成该内容的答题
    # 这里需要创建一个答题记录表来存储用户答题状态
    # 为简化演示，我们返回一个示例结构
    
    # 检查是否做过答题
    from sqlalchemy import text
    result = db.execute(text("""
        SELECT COUNT(*) as count FROM point_transactions 
        WHERE user_id = :user_id 
        AND related_id = :content_id 
        AND operation_type = 'quiz_completion'
    """), {"user_id": user_id, "content_id": content_id}).fetchone()
    
    has_completed = result[0] > 0
    
    return {
        "content_id": content_id,
        "has_started": len(db.query(Question).filter(Question.content_id == content_id).all()) > 0,
        "has_completed": has_completed,
        "progress": 100 if has_completed else 0
    }
