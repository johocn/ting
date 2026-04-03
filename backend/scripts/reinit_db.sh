#!/bin/bash

echo "=== 重新初始化Ting学习平台数据库 ==="

# 检查PostgreSQL容器状态
if ! docker ps | grep -q "ting_postgres"; then
    echo "错误: ting_postgres容器未运行"
    exit 1
fi

echo "使用ting_user用户连接数据库..."

# 首先检查ting_db数据库是否存在
DB_EXISTS=$(docker exec ting_postgres psql -U ting_user -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='ting_db';" 2>/dev/null)

if [ "$DB_EXISTS" != "1" ]; then
    echo "错误: ting_db数据库不存在，需要使用正确的初始化方法"
    echo "尝试重新创建容器..."
    
    # 停止当前容器
    docker stop ting_postgres
    docker rm ting_postgres
    
    # 重新创建容器，这次使用正确的环境变量
    docker run -d \
        --name ting_postgres \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_PASSWORD=postgres \
        -e POSTGRES_DB=postgres \
        -p 5432:5432 \
        -v ting_postgres_data:/var/lib/postgresql/data \
        postgres:13
    
    # 等待数据库启动
    echo "等待数据库启动..."
    sleep 10
    
    # 创建ting_db数据库和用户
    docker exec -i ting_postgres psql -U postgres -d postgres << SQL
CREATE DATABASE ting_db;
CREATE USER ting_user WITH PASSWORD 'ting_password';
GRANT ALL PRIVILEGES ON DATABASE ting_db TO ting_user;
\c ting_db
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SQL

    echo "数据库和用户创建成功"
else
    echo "ting_db数据库已存在"
fi

echo "=== 数据库初始化完成 ==="