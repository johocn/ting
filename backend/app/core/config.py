from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # 项目配置
    PROJECT_NAME: str = "Ting Learning Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/db")
    
    # Redis配置
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # JWT配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 微信配置
    WECHAT_APP_ID: str = os.getenv("WECHAT_APP_ID", "")
    WECHAT_APP_SECRET: str = os.getenv("WECHAT_APP_SECRET", "")
    
    # CORS配置
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://admin.yourdomain.com",
        "https://mobile.yourdomain.com"
    ]

settings = Settings()
