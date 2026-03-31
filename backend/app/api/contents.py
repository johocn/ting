from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.contents import Content, Question, ContentQuizConfig
from app.schemas.contents import ContentCreate, ContentUpdate, QuestionCreate, QuestionUpdate

router = APIRouter(prefix="/contents", tags=["contents"])

@router.get("/", response_model=List[dict])
async def get_contents(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """获取内容列表"""
    contents = db.query(Content).offset(skip).limit(limit).all()
    return contents

@router.get("/{content_id}", response_model=dict)
async def get_content(content_id: int, db: Session = Depends(get_db)):
    """获取单个内容详情"""
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")
    return content

@router.post("/", response_model=dict)
async def create_content(content: ContentCreate, db: Session = Depends(get_db)):
    """创建新内容"""
    db_content = Content(**content.model_dump())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

@router.put("/{content_id}", response_model=dict)
async def update_content(
    content_id: int, 
    content_update: ContentUpdate, 
    db: Session = Depends(get_db)
):
    """更新内容"""
    db_content = db.query(Content).filter(Content.id == content_id).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="内容不存在")
    
    for key, value in content_update.model_dump(exclude_unset=True).items():
        setattr(db_content, key, value)
    
    db.commit()
    return db_content

@router.delete("/{content_id}")
async def delete_content(content_id: int, db: Session = Depends(get_db)):
    """删除内容"""
    db_content = db.query(Content).filter(Content.id == content_id).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="内容不存在")
    
    db.delete(db_content)
    db.commit()
    return {"message": "内容删除成功"}

@router.get("/{content_id}/questions", response_model=List[dict])
async def get_content_questions(content_id: int, db: Session = Depends(get_db)):
    """获取内容相关的问题"""
    questions = db.query(Question).filter(Question.content_id == content_id).all()
    return questions

@router.post("/{content_id}/questions", response_model=dict)
async def create_question(
    content_id: int, 
    question: QuestionCreate, 
    db: Session = Depends(get_db)
):
    """创建问题"""
    # 验证内容是否存在
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")
    
    db_question = Question(content_id=content_id, **question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/{content_id}/quiz-config", response_model=dict)
async def get_quiz_config(content_id: int, db: Session = Depends(get_db)):
    """获取内容的答题配置"""
    config = db.query(ContentQuizConfig).filter(
        ContentQuizConfig.content_id == content_id
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="答题配置不存在")
    
    return config

@router.put("/{content_id}/quiz-config", response_model=dict)
async def update_quiz_config(
    content_id: int, 
    config_update: dict, 
    db: Session = Depends(get_db)
):
    """更新内容的答题配置"""
    config = db.query(ContentQuizConfig).filter(
        ContentQuizConfig.content_id == content_id
    ).first()
    
    if not config:
        # 如果配置不存在，创建新配置
        config = ContentQuizConfig(content_id=content_id, **config_update)
        db.add(config)
    else:
        # 更新现有配置
        for key, value in config_update.items():
            setattr(config, key, value)
    
    db.commit()
    return config
