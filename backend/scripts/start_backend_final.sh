#!/bin/bash

echo "=== 启动Ting后端服务 ==="

# 检查端口是否被占用
if lsof -Pi :8001 -sTCP:LISTEN -t > /dev/null; then
    echo "停止占用端口8001的进程..."
    PID=$(lsof -t -i:8001)
    kill -9 $PID 2>/dev/null || echo "没有进程在端口8001上运行"
fi

# 检查容器是否已存在，如果存在则先停止并删除
if [ "$(docker ps -aq -f name=^ting_backend_prod$)" ]; then
    echo "停止现有容器..."
    docker stop ting_backend_prod 2>/dev/null
    docker rm ting_backend_prod 2>/dev/null
fi

# 构建Docker镜像（如果还没有的话）
echo "检查Docker镜像..."
if [ "$(docker images -q ting-backend 2>/dev/null)" = "" ]; then
    echo "构建Docker镜像..."
    cd /home/admin/.openclaw/workspace/ting/backend
    docker build -t ting-backend .
else
    echo "使用现有镜像 ting-backend"
fi

# 运行容器
echo "启动Ting后端服务..."
docker run -d \
    --name ting_backend_prod \
    --network bridge \
    -e DATABASE_URL=postgresql://ting_user:ting_password@host.docker.internal:5432/ting_db \
    -e REDIS_URL=redis://host.docker.internal:6379/0 \
    -e SECRET_KEY=your-super-secret-key-change-this-in-production \
    -e DEBUG=false \
    -p 8001:8000 \
    ting-backend

echo "等待服务启动..."
sleep 15

# 检查服务是否运行
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✓ Ting后端服务运行正常"
    echo "API地址: http://localhost:8001"
    echo "服务状态: docker ps | grep ting_backend_prod"
else
    echo "✗ 服务启动失败，查看日志:"
    docker logs ting_backend_prod
    echo "检查容器状态: docker ps -a | grep ting_backend_prod"
fi