#!/bin/bash

echo "=== 停止Ting后端服务 ==="

# 停止容器
if [ "$(docker ps -aq -f name=^ting_backend_prod$)" ]; then
    echo "停止ting_backend_prod容器..."
    docker stop ting_backend_prod
    docker rm ting_backend_prod
    echo "✓ 服务已停止"
else
    echo "未发现ting_backend_prod容器"
fi

# 检查test_ting_backend容器（之前的测试容器）
if [ "$(docker ps -aq -f name=^test_ting_backend$)" ]; then
    echo "停止test_ting_backend容器..."
    docker stop test_ting_backend
    docker rm test_ting_backend
    echo "之前测试容器已清理"
fi

echo "服务停止完成"