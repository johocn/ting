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
    echo "错误: ting_postgres服务未运行"
    exit 1
fi

if ! docker ps | grep -q "ting_redis"; then
    echo "错误: ting_redis服务未运行"
    exit 1
fi

echo "✓ 所有依赖服务正常运行"

# 2. 检查端口占用
PORTS=("8001" "3001")
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

echo "✓ 端口检查通过"

# 3. 初始化数据库（如果需要）
DB_INIT_FILE="/home/admin/.openclaw/workspace/ting/backend/.db_initialized"
if [ ! -f "$DB_INIT_FILE" ]; then
    echo "初始化数据库..."
    cd /home/admin/.openclaw/workspace/ting/backend
    # 检查数据库是否已存在，如果不存在则创建
    python -c "
import psycopg2
import os
from app.core.config import settings
import subprocess

# 尝试连接数据库 - 使用Docker服务
try:
    # 连接到宿主机上的PostgreSQL
    conn = psycopg2.connect(
        host='localhost',  # 由于我们知道PostgreSQL在Docker中运行，使用localhost
        port=5432,
        user='postgres',
        password='postgres',  # 请根据实际密码修改，或者从环境变量获取
        database='postgres'
    )
    cur = conn.cursor()
    
    # 检查数据库是否存在
    cur.execute(\"SELECT 1 FROM pg_database WHERE datname='ting_db'\")
    exists = cur.fetchone()
    
    if not exists:
        print('创建ting_db数据库...')
        cur.execute('CREATE DATABASE ting_db')
        print('数据库ting_db创建成功')
    else:
        print('ting_db数据库已存在')
    
    # 检查用户是否存在
    cur.execute(\"SELECT 1 FROM pg_user WHERE usename='ting_user'\")
    user_exists = cur.fetchone()
    
    if not user_exists:
        print('创建ting_user用户...')
        cur.execute(\"CREATE USER ting_user WITH PASSWORD 'ting_password'\")
        cur.execute('GRANT ALL PRIVILEGES ON DATABASE ting_db TO ting_user')
        print('用户ting_user创建并授权成功')
    else:
        print('ting_user用户已存在')
    
    conn.commit()
    cur.close()
    conn.close()
except Exception as e:
    print(f'数据库初始化失败: {e}')
    # 尝试使用Docker exec方式访问数据库容器
    try:
        print('尝试通过Docker容器连接...')
        result = subprocess.run([
            'docker', 'exec', 'ting_postgres', 
            'psql', '-U', 'postgres', '-c', 
            \"SELECT 1 FROM pg_database WHERE datname='ting_db'\"
        ], capture_output=True, text=True)
        
        if 'ting_db' not in result.stdout:
            print('通过Docker创建ting_db数据库...')
            subprocess.run([
                'docker', 'exec', 'ting_postgres',
                'psql', '-U', 'postgres', '-c',
                'CREATE DATABASE ting_db;'
            ])
            print('数据库创建成功')
        
        # 创建用户
        subprocess.run([
            'docker', 'exec', 'ting_postgres',
            'psql', '-U', 'postgres', '-c',
            \"CREATE USER IF NOT EXISTS ting_user WITH PASSWORD 'ting_password';\"
        ])
        subprocess.run([
            'docker', 'exec', 'ting_postgres',
            'psql', '-U', 'postgres', '-c',
            'GRANT ALL PRIVILEGES ON DATABASE ting_db TO ting_user;'
        ])
        print('用户创建并授权成功')
    except Exception as docker_e:
        print(f'通过Docker初始化也失败: {docker_e}')
        exit(1)
"
    touch "$DB_INIT_FILE"
    echo "数据库初始化完成"
else
    echo "数据库已初始化，跳过"
fi

# 4. 返回到工作目录
cd /home/admin/.openclaw/workspace/ting/backend

# 5. 检查并创建必要目录
mkdir -p logs uploads

# 6. 创建docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  ting-backend:
    build: .
    container_name: ting_backend
    ports:
      - "8001:8000"
    environment:
      - DATABASE_URL=postgresql://ting_user:ting_password@ting_postgres:5432/ting_db
      - REDIS_URL=redis://ting_redis:6379/0
      - SECRET_KEY=your-super-secret-key-change-this-in-production
      - DEBUG=false
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    networks:
      - ting-network
    restart: unless-stopped

networks:
  ting-network:
    driver: bridge
EOF

# 7. 创建Dockerfile
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

# 8. 构建并启动服务
echo "构建并启动服务..."
docker-compose up -d --build

# 9. 等待服务启动
echo "等待服务启动..."
sleep 15

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
echo "服务日志: docker-compose logs -f"