# 开发者文档

## 📖 项目概述

Ting Learning Platform 是一个基于视频音频学习赚积分的综合性学习平台，采用前后端分离架构，支持微信登录、邀请推广、积分商城、线下核销等功能。

## 🏗️ 技术架构

### 1. 技术栈

#### 后端技术栈
- **语言**: Python 3.9+
- **框架**: FastAPI
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy
- **缓存**: Redis
- **消息队列**: Celery (可选)
- **任务调度**: APScheduler
- **认证**: JWT
- **API文档**: Swagger/OpenAPI

#### 前端技术栈
- **框架**: Vue 3 + Composition API
- **UI库**: Element Plus
- **状态管理**: Vuex
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **构建工具**: Vite/Webpack

#### 移动端技术栈
- **框架**: UniApp
- **小程序**: 微信小程序原生支持

#### 部署技术栈
- **容器**: Docker
- **编排**: Docker Compose
- **反向代理**: Nginx
- **CI/CD**: GitHub Actions

### 2. 项目结构

```
ting-platform/
├── backend/                 # 后端服务
│   ├── app/                # 应用代码
│   │   ├── api/           # API接口定义
│   │   ├── models/        # 数据模型
│   │   ├── schemas/       # Pydantic数据验证模型
│   │   ├── core/          # 核心配置
│   │   ├── database/      # 数据库配置
│   │   ├── services/      # 业务服务层
│   │   └── utils/         # 工具函数
│   ├── migrations/         # 数据库迁移
│   ├── tests/             # 测试代码
│   ├── requirements.txt    # Python依赖
│   └── main.py            # 应用入口
├── frontend/              # 前端项目
│   ├── admin/             # 管理后台
│   │   ├── src/          # 源码
│   │   │   ├── api/      # API接口封装
│   │   │   ├── views/    # 页面组件
│   │   │   ├── components/ # 通用组件
│   │   │   ├── router/   # 路由配置
│   │   │   ├── store/    # 状态管理
│   │   │   └── utils/    # 工具函数
│   │   ├── public/       # 静态资源
│   │   └── package.json  # 依赖配置
│   └── mobile/            # 移动端
├── docker/                # Docker配置
├── docs/                 # 文档
├── scripts/              # 脚本
└── tests/                # 测试相关
```

## 🚀 开发环境搭建

### 1. 环境准备

#### 1.1 安装依赖

```bash
# 系统依赖
sudo apt-get update
sudo apt-get install python3 python3-pip postgresql redis-server

# Python虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装Python依赖
pip install -r backend/requirements.txt

# 安装前端依赖
cd frontend/admin
npm install
```

#### 1.2 配置环境变量

创建 `.env` 文件：

```bash
# backend/.env
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=true
```

### 2. 数据库配置

#### 2.1 PostgreSQL设置

```sql
-- 创建数据库
CREATE DATABASE ting_db;
CREATE USER ting_user WITH PASSWORD 'ting_password';
GRANT ALL PRIVILEGES ON DATABASE ting_db TO ting_user;
```

#### 2.2 数据库迁移

```bash
# 初始化数据库
cd backend
alembic init migrations

# 生成迁移脚本
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 3. 启动开发服务

#### 3.1 后端开发

```bash
# 启动后端服务
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3.2 前端开发

```bash
# 启动前端开发服务器
cd frontend/admin
npm run serve
```

## 🏗️ 代码规范

### 1. Python代码规范

#### 1.1 命名规范
- 类名: `CamelCase`
- 函数名: `snake_case`
- 常量: `UPPER_SNAKE_CASE`
- 私有成员: `_private_name`

#### 1.2 代码风格
```python
# 导入顺序
import stdlib
import third-party
import local

# 使用类型提示
def get_user(user_id: int) -> User:
    ...

# 使用docstring
def calculate_points(duration: int) -> int:
    """
    Calculate points based on watch duration
    
    Args:
        duration: Watch duration in seconds
        
    Returns:
        Calculated points
    """
    return duration // 60 * 5
```

#### 1.3 异常处理
```python
from fastapi import HTTPException

def validate_input(data: dict):
    if not data.get("required_field"):
        raise HTTPException(
            status_code=400,
            detail="Required field is missing"
        )
```

### 2. JavaScript代码规范

#### 2.1 Vue组件规范
```javascript
// 组件命名: PascalCase
export default {
  name: 'UserCard',
  
  // Props定义
  props: {
    user: {
      type: Object,
      required: true
    },
    size: {
      type: String,
      default: 'normal'
    }
  },
  
  // 组件数据
  setup() {
    const data = ref({})
    
    return {
      data
    }
  }
}
```

#### 2.2 API调用规范
```javascript
// API封装
import request from '@/utils/request'

export const userApi = {
  getUserInfo(userId) {
    return request({
      url: `/users/${userId}`,
      method: 'get'
    })
  }
}
```

## 📊 数据库设计

### 1. 核心表结构

#### 1.1 用户表 (users)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(100) UNIQUE,
    integral INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    is_member BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 1.2 内容表 (contents)
```sql
CREATE TABLE contents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    url TEXT NOT NULL,
    duration INTEGER DEFAULT 0,
    category VARCHAR(50),
    reward_points_per_minute INTEGER DEFAULT 5,
    status BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 1.3 积分账户表 (user_point_accounts)
```sql
CREATE TABLE user_point_accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total_points INTEGER DEFAULT 0,
    available_points INTEGER DEFAULT 0,
    frozen_points INTEGER DEFAULT 0,
    expired_points INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. 索引优化

```sql
-- 用户表索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_email ON users(email);

-- 内容表索引
CREATE INDEX idx_contents_category ON contents(category);
CREATE INDEX idx_contents_status ON contents(status);

-- 积分流水表索引
CREATE INDEX idx_transactions_user_id ON point_transactions(user_id);
CREATE INDEX idx_transactions_type ON point_transactions(transaction_type);
CREATE INDEX idx_transactions_date ON point_transactions(created_at);
```

## 🔧 API设计规范

### 1. RESTful API设计

#### 1.1 URL规范
```
# 资源集合
GET /api/v1/users          # 获取用户列表
POST /api/v1/users         # 创建用户

# 单个资源
GET /api/v1/users/{id}     # 获取単个用户
PUT /api/v1/users/{id}     # 更新用户
DELETE /api/v1/users/{id}  # 删除用户
```

#### 1.2 响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### 1.3 错误处理
```python
from fastapi import HTTPException

# 业务错误
raise HTTPException(
    status_code=400,
    detail="Invalid input data"
)

# 权限错误
raise HTTPException(
    status_code=403,
    detail="Insufficient permissions"
)

# 资源不存在
raise HTTPException(
    status_code=404,
    detail="Resource not found"
)
```

### 2. 认证授权

#### 2.1 JWT认证
```python
from fastapi import Depends
from fastapi.security import HTTPBearer
from jose import jwt

security = HTTPBearer()

def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return get_user(user_id)
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

#### 2.2 权限控制
```python
def require_permission(permission: str):
    def permission_checker(func):
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not check_permission(current_user, permission):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, **kwargs)
        return wrapper
    return permission_checker
```

## 🧪 测试策略

### 1. 测试层级

#### 1.1 单元测试
```python
import pytest
from app.models.users import User

def test_create_user(db_session):
    user = User(username="test", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert user.username == "test"
```

#### 1.2 集成测试
```python
def test_user_registration(client):
    response = client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "password": "password123",
        "phone": "13800138000"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
```

#### 1.3 端到端测试
```python
def test_complete_learning_flow(browser):
    # 用户注册
    browser.visit("/register")
    browser.fill("username", "testuser")
    browser.fill("password", "password123")
    browser.click("submit")
    
    # 观看视频
    browser.click("video1")
    browser.wait_for_video_to_finish()
    
    # 验证积分获取
    assert browser.find(".points-balance").text == "50"
```

### 2. 测试覆盖率

```bash
# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html

# 检查覆盖率
coverage report
```

## 🔒 安全措施

### 1. 输入验证
```python
from pydantic import BaseModel, validator

class UserCreate(BaseModel):
    username: str
    phone: str
    password: str
    
    @validator('phone')
    def validate_phone(cls, v):
        if not validate_phone_format(v):
            raise ValueError('Invalid phone format')
        return v
```

### 2. SQL注入防护
```python
# 使用ORM查询，避免原生SQL
user = db.query(User).filter(User.id == user_id).first()

# 如需原生SQL，使用参数化查询
result = db.execute(
    "SELECT * FROM users WHERE id = :user_id",
    {"user_id": user_id}
)
```

### 3. XSS防护
```python
# FastAPI自动转义HTML
from markupsafe import escape

def sanitize_input(text: str) -> str:
    return escape(text)
```

## 🚀 部署指南

### 1. 生产环境配置

#### 1.1 环境变量
```bash
# 生产环境变量
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://prod_user:prod_password@prod_host:5432/prod_db
```

#### 1.2 性能优化
```python
# Gunicorn配置
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:8000"
timeout = 30
max_requests = 1000
max_requests_jitter = 100
```

### 2. 监控告警

#### 2.1 日志配置
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

#### 2.2 健康检查
```python
@app.get("/health")
async def health_check():
    # 检查数据库连接
    try:
        db.execute("SELECT 1")
    except:
        return {"status": "error", "database": "unreachable"}
    
    return {"status": "healthy", "database": "connected"}
```

## 📦 扩展开发

### 1. 新增功能模块

#### 1.1 创建API模块
```python
# backend/app/api/new_module.py
from fastapi import APIRouter

router = APIRouter(prefix="/new-module", tags=["new-module"])

@router.get("/")
async def get_new_module():
    return {"message": "New module endpoint"}
```

#### 1.2 注册API路由
```python
# backend/app/api/__init__.py
from app.api import new_module

router.include_router(new_module.router)
```

### 2. 数据模型扩展

```python
# backend/app/models/new_models.py
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class NewEntity(Base):
    __tablename__ = "new_entities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 3. 服务层开发

```python
# backend/app/services/new_service.py
from sqlalchemy.orm import Session
from app.models.new_models import NewEntity

def create_new_entity(db: Session, name: str, description: str = None):
    entity = NewEntity(name=name, description=description)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity
```

## 🛠️ 工具脚本

### 1. 数据迁移脚本
```bash
#!/bin/bash
# scripts/migrate.sh

echo "Starting database migration..."
cd backend
alembic upgrade head
echo "Migration completed!"
```

### 2. 数据备份脚本
```bash
#!/bin/bash
# scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="ting_db"

echo "Creating backup for $DB_NAME..."
pg_dump -U ting_user $DB_NAME > $BACKUP_DIR/backup_$DATE.sql
echo "Backup completed: backup_$DATE.sql"
```

### 3. 性能测试脚本
```python
# scripts/performance_test.py
import asyncio
import aiohttp
import time

async def performance_test():
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(100):  # 100个并发请求
            task = asyncio.create_task(
                session.get('http://localhost:8000/api/v1/contents')
            )
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
    end_time = time.time()
    print(f"Completed 100 requests in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(performance_test())
```

## 📚 参考资料

- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [Vue 3官方文档](https://v3.vuejs.org/)
- [Element Plus文档](https://element-plus.org/)
- [PostgreSQL文档](https://www.postgresql.org/docs/)
- [Docker文档](https://docs.docker.com/)

---

**注意**: 本文档持续更新，请以最新版本为准。
