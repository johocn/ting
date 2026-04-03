#!/bin/bash

set -e  # 遇到错误立即退出

echo "=== 启动Ting学习平台服务 ==="

# 1. 检查依赖服务
echo "检查依赖服务..."
if ! docker info > /dev/null 2>&1; then
    echo "错误: Docker服务未运行"
    exit 1
fi

# 检查Docker中的PostgreSQL和Redis服务
if ! docker ps | grep -q "ting_postgres"; then
    echo "错误: 全局ting_postgres服务未运行"
    echo "请先启动全局数据库服务"
    exit 1
fi

if ! docker ps | grep -q "ting_redis"; then
    echo "错误: 全局ting_redis服务未运行"
    echo "请先启动全局Redis服务"
    exit 1
fi

echo "✓ 所有依赖服务正常运行"

# 2. 检查端口占用
PORTS=("8001")
for port in "${PORTS[@]}"; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; then
        echo "警告: 端口 $port 已被占用，尝试停止相关服务..."
        PID=$(lsof -t -i:$port)
        if [ ! -z "$PID" ]; then
            echo "停止占用端口 $port 的进程 (PID: $PID)"
            kill -9 $PID
            sleep 2
        fi
    fi
done

# 3. 初始化数据库（如果需要）
DB_INIT_FILE="/home/admin/.openclaw/workspace/ting/backend/.db_initialized"
if [ ! -f "$DB_INIT_FILE" ]; then
    echo "初始化数据库..."
    cd /home/admin/.openclaw/workspace/ting/backend
    
    # 使用Docker exec方式访问数据库容器
    # 检查ting_db数据库是否存在 (使用正确的用户)
    DB_EXISTS=$(docker exec ting_postgres psql -U ting_user -tAc "SELECT 1 FROM pg_database WHERE datname='ting_db';" 2>/dev/null)
    
    if [ "$DB_EXISTS" != "1" ]; then
        echo "创建ting_db数据库..."
        # 使用postgres用户创建数据库
        docker exec ting_postgres psql -U postgres -c "CREATE DATABASE ting_db;" 2>/dev/null || echo "数据库可能已存在"
        echo "数据库ting_db创建成功"
    else
        echo "ting_db数据库已存在"
    fi
    
    # 检查用户是否存在 (使用postgres用户)
    USER_EXISTS=$(docker exec ting_postgres psql -U postgres -tAc "SELECT 1 FROM pg_user WHERE usename='ting_user';" 2>/dev/null)
    
    if [ "$USER_EXISTS" != "1" ]; then
        echo "创建ting_user用户..."
        docker exec ting_postgres psql -U postgres -c "CREATE USER ting_user WITH PASSWORD 'ting_password';" 2>/dev/null || echo "用户可能已存在"
        docker exec ting_postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ting_db TO ting_user;" 2>/dev/null || echo "权限可能已授予"
        echo "用户ting_user创建并授权成功"
    else
        echo "ting_user用户已存在"
    fi
    
    touch "$DB_INIT_FILE"
    echo "数据库初始化完成"
else
    echo "数据库已初始化，跳过"
fi

# 4. 返回到工作目录
cd /home/admin/.openclaw/workspace/ting/backend

# 5. 检查并创建必要目录
mkdir -p logs uploads data/postgres data/redis

# 6. 创建Dockerfile（如果不存在）
if [ ! -f "Dockerfile" ]; then
    cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 运行应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
    echo "Dockerfile已创建"
fi

# 7. 检查requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "创建requirements.txt..."
    cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
redis==5.0.1
alembic==1.13.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
requests==2.31.0
async-exit-stack==1.0.1
async-generator==1.10
email-validator==2.1.0
aiofiles==23.2.1
EOF
fi

# 8. 构建并启动服务
echo "构建并启动服务..."
docker-compose up -d --build

# 9. 等待服务启动
echo "等待服务启动..."
sleep 20

# 10. 验证服务状态
echo "验证服务状态..."
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✓ Backend服务运行正常"
else
    echo "✗ Backend服务启动失败，显示日志:"
    docker-compose logs ting-backend
    exit 1
fi

echo "=== Ting学习平台服务启动完成 ==="
echo "Backend API: http://localhost:8001"
echo "服务状态: docker-compose ps"
echo "服务日志: docker-compose logs -f ting-backend"