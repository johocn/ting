# 部署文档

## 🚀 部署概述

本文档详细介绍了 Ting Learning Platform 的部署流程，包括开发环境、测试环境和生产环境的配置。

## 🏗️ 环境要求

### 系统要求
- **操作系统**: Linux (Ubuntu 18.04+, CentOS 7+) 或 macOS
- **内存**: 最小 4GB，推荐 8GB+
- **磁盘**: 最小 20GB 可用空间
- **CPU**: 双核及以上

### 软件要求
- **Docker**: 19.03+ (推荐 20.10+)
- **Docker Compose**: 1.29+ (推荐 2.0+)
- **Git**: 2.0+
- **Node.js**: 14+ (前端构建需要)
- **Python**: 3.8+ (后端运行需要)

## 📦 部署方式

### 1. Docker Compose 部署 (推荐)

#### 1.1 环境准备

```bash
# 克隆项目
git clone https://github.com/johocn/ting.git
cd ting

# 检查 Docker 版本
docker --version
docker-compose --version
```

#### 1.2 配置环境变量

```bash
# 复制环境配置文件
cp .env.example .env

# 编辑环境变量
vim .env
```

**环境变量说明**:
```bash
# 数据库配置
POSTGRES_DB=ting_db
POSTGRES_USER=ting_user
POSTGRES_PASSWORD=ting_password

# Redis配置
REDIS_URL=redis://redis:6379

# JWT密钥 (生产环境务必修改)
SECRET_KEY=your-very-secure-secret-key-change-in-production

# API基础URL
API_BASE_URL=http://localhost:8000

# 前端配置
FRONTEND_BASE_URL=http://localhost:3000

# 微信配置
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret
```

#### 1.3 启动服务

```bash
# 构建并启动所有服务
docker-compose up -d

# 检查服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
```

#### 1.4 初始化数据库

```bash
# 进入后端容器
docker-compose exec backend bash

# 运行数据库迁移
alembic upgrade head

# 退出容器
exit
```

#### 1.5 访问服务

- **管理后台**: http://localhost:3000
- **API接口**: http://localhost:8000
- **数据库**: localhost:5432
- **Redis**: localhost:6379

### 2. 生产环境部署

#### 2.1 生产环境配置

创建 `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    container_name: ting_postgres_prod
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - /data/postgresql:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - ting_network

  redis:
    image: redis:6-alpine
    container_name: ting_redis_prod
    volumes:
      - /data/redis:/data
    restart: unless-stopped
    networks:
      - ting_network

  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: ting_backend_prod
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
    volumes:
      - /app/logs:/app/logs
    restart: unless-stopped
    depends_on:
      - postgres
      - redis
    networks:
      - ting_network

  admin-frontend:
    build:
      context: .
      dockerfile: frontend/admin/Dockerfile
    container_name: ting_admin_frontend_prod
    restart: unless-stopped
    networks:
      - ting_network

  nginx:
    image: nginx:alpine
    container_name: ting_nginx_prod
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /etc/letsencrypt:/etc/letsencrypt
    restart: unless-stopped
    depends_on:
      - backend
      - admin-frontend
    networks:
      - ting_network

networks:
  ting_network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

#### 2.2 SSL证书配置

```bash
# 安装Certbot
sudo apt-get update
sudo apt-get install certbot

# 获取SSL证书 (替换为你的域名)
sudo certbot certonly --standalone -d yourdomain.com

# 配置Nginx SSL
# nginx.conf
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # 其他配置...
}
```

#### 2.3 启动生产环境

```bash
# 使用生产配置启动
docker-compose -f docker-compose.prod.yml up -d

# 检查服务状态
docker-compose -f docker-compose.prod.yml ps
```

### 3. Kubernetes 部署 (高级)

#### 3.1 准备K8s配置

创建 `k8s/` 目录并配置部署文件:

```yaml
# k8s/postgres-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:13
        env:
        - name: POSTGRES_DB
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: db
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP
```

## 🛠️ 配置管理

### 1. 环境变量管理

```bash
# 开发环境
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=debug

# 生产环境
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info
```

### 2. 数据库配置

```bash
# 数据库连接池
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
DB_POOL_RECYCLE=3600

# 数据库备份
DB_BACKUP_INTERVAL=24h
DB_BACKUP_RETENTION=30d
```

### 3. 缓存配置

```bash
# Redis配置
REDIS_MAX_MEMORY=512mb
REDIS_EXPIRE_TIME=3600
REDIS_CONNECTION_TIMEOUT=5
```

## 🚦 健康检查

### 1. 服务健康检查

```bash
# 检查后端服务
curl -f http://localhost:8000/health

# 检查前端服务
curl -f http://localhost:3000

# 检查数据库连接
docker-compose exec postgres pg_isready

# 检查Redis连接
docker-compose exec redis redis-cli ping
```

### 2. 监控指标

- **API响应时间**: < 200ms
- **数据库连接数**: < 80%最大连接数
- **内存使用率**: < 80%
- **CPU使用率**: < 80%

## 🔧 运维操作

### 1. 日志管理

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs postgres

# 实时查看日志
docker-compose logs -f backend

# 日志轮转配置
# docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 2. 备份恢复

```bash
# 数据库备份
docker-compose exec postgres pg_dump -U ting_user ting_db > backup.sql

# 数据库恢复
cat backup.sql | docker-compose exec -T postgres psql -U ting_user ting_db

# 自动备份脚本
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U ting_user -d ting_db > /backup/ting_backup_$DATE.sql
```

### 3. 性能优化

```bash
# 数据库索引优化
CREATE INDEX idx_contents_category ON contents(category);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_points_user_id ON point_transactions(user_id);

# Redis缓存策略
# 1. 热点数据缓存
# 2. 会话数据存储
# 3. 频率限制计数器
```

### 4. 安全配置

```bash
# 防火墙配置
ufw allow 80
ufw allow 443
ufw allow 22

# SSH安全
# 禁用密码登录，使用密钥认证

# 数据库安全
# 1. 使用专用用户
# 2. 限制权限
# 3. 定期更新密码
```

## 🔄 更新部署

### 1. 蓝绿部署

```bash
# 部署新版本到备用环境
docker-compose -f docker-compose.staging.yml up -d

# 测试新版本
curl -f http://staging.yourdomain.com/health

# 切换流量到新版本
# 更新负载均衡器指向新版本

# 回滚（如需要）
# 将流量切换回旧版本
```

### 2. 滚动更新

```bash
# 更新后端服务
docker-compose up -d --no-deps backend

# 等待新实例就绪
sleep 30

# 停止旧实例
docker-compose kill --signal=SIGHUP backend_old
```

## 📊 监控告警

### 1. 系统监控

```bash
# 使用Prometheus + Grafana
# 1. 配置Prometheus抓取指标
# 2. 创建Grafana仪表板
# 3. 设置告警规则
```

### 2. 业务监控

```bash
# 关键业务指标
- 用户注册数
- 内容播放量
- 积分兑换数
- 核销成功率
- API响应时间
```

## 🚨 故障处理

### 1. 常见问题

**问题**: 服务启动失败
**解决方案**: 
```bash
# 检查日志
docker-compose logs

# 检查端口占用
netstat -tlnp | grep :8000

# 重启服务
docker-compose restart backend
```

**问题**: 数据库连接失败
**解决方案**:
```bash
# 检查数据库状态
docker-compose ps postgres

# 检查连接字符串
docker-compose exec backend env | grep DATABASE_URL
```

### 2. 紧急预案

- **数据库故障**: 启动备用数据库，恢复数据
- **服务宕机**: 启动备用实例，切换流量
- **安全事件**: 立即隔离，启动应急预案

## 📋 部署检查清单

- [ ] 环境变量配置正确
- [ ] 数据库连接正常
- [ ] Redis连接正常
- [ ] SSL证书有效
- [ ] 域名解析正确
- [ ] 防火墙配置正确
- [ ] 备份策略生效
- [ ] 监控告警配置
- [ ] 安全配置完成
- [ ] 性能基准测试通过

---

**注意**: 生产环境部署前请务必在测试环境充分验证！
