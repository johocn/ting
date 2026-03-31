from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
import hashlib
from app.database import get_db
from app.models.users import User
from app.schemas.auth import UserCreate, UserLogin
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 创建新用户
    hashed_password = hashlib.sha256(user_data.password.encode()).hexdigest()
    new_user = User(
        username=user_data.username,
        password_hash=hashed_password,
        phone=user_data.phone
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # 生成JWT token
    token = create_access_token(data={"sub": str(new_user.id)})
    
    return {
        "user_id": new_user.id,
        "username": new_user.username,
        "token": token
    }

@router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    hashed_password = hashlib.sha256(user_data.password.encode()).hexdigest()
    if user.password_hash != hashed_password:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    # 生成JWT token
    token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "user_id": user.id,
        "username": user.username,
        "token": token
    }

def create_access_token(data: dict):
    """创建JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt
