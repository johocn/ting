# Ting Learning Platform 安装指南

## 📋 系统要求

### 服务器配置
- **操作系统**: Ubuntu 18.04+ / CentOS 7+ / macOS 10.14+ / Windows 10+
- **CPU**: 双核及以上
- **内存**: 4GB RAM (推荐 8GB+)
- **磁盘**: 20GB 可用空间
- **网络**: 稳定的互联网连接

### 软件依赖
- **Docker**: 19.03.0+
- **Docker Compose**: 1.29.0+
- **Git**: 2.0+
- **Node.js**: 14+ (前端构建需要)
- **Python**: 3.8+ (后端运行需要)

## 🚀 快速安装

### 1. 克隆项目

```bash
# 克隆项目到本地
git clone https://github.com/johocn/ting.git
cd ting
```

### 2. 配置环境

```bash
# 复制环境配置文件
cp .env.example .env

# 编辑环境配置
nano .env
```

**重要配置项说明**:

```bash
# 数据库配置
POSTGRES_DB=ting_db
POSTGRES_USER=ting_user
POSTGRES_PASSWORD=your_secure_password

# Redis配置
REDIS_URL=redis://redis:6379/0

# JWT密钥 (生产环境务必更换!)
SECRET_KEY=your_very_secure_secret_key_change_this_in_production

# 微信配置 (可选，如需微信功能)
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret

# 业务配置
POINTS_PER_VIDEO_MINUTE=5      # 观看视频每分钟积分
POINTS_PER_AUDIO_MINUTE=3      # 收听音频每分钟积分
POINTS_PER_CORRECT_ANSWER=20   # 答题正确积分
```

### 3. 构建并启动服务

```bash
# 构建并启动所有服务
docker-compose up -d

# 检查服务状态
docker-compose ps
```

### 4. 初始化数据库

```bash
# 等待数据库服务启动
sleep 30

# 执行数据库迁移
docker-compose exec backend alembic upgrade head
```

### 5. 访问服务

- **管理后台**: http://localhost:3000
- **API接口**: http://localhost:8000
- **数据库**: localhost:5432
- **Redis**: localhost:6379

## 🏗️ 生产环境部署

### 1. 生产环境配置

```bash
# 创建生产环境配置
cp .env.example .env.prod

# 编辑生产环境配置
nano .env.prod
```

**生产环境配置要点**:

```bash
# 安全配置
DEBUG=false
ENVIRONMENT=production
LOG_LEVEL=WARNING

# 数据库配置 (建议使用外部数据库)
DATABASE_URL=postgresql://user:password@external-db-host:5432/dbname

# JWT配置 (更强的安全性)
SECRET_KEY=your_very_strong_production_secret_key_here

# API配置
API_V1_STR=/api/v1
PROJECT_NAME=Ting Learning Platform
VERSION=1.0.0
```

### 2. 使用生产配置启动

```bash
# 使用生产配置启动
docker-compose -f docker-compose.prod.yml up -d

# 或者使用环境变量
COMPOSE_FILE=docker-compose.prod.yml docker-compose up -d
```

### 3. 配置SSL (推荐)

```bash
# 安装certbot
sudo apt-get update
sudo apt-get install certbot

# 获取SSL证书
sudo certbot certonly --standalone -d yourdomain.com

# 配置Nginx SSL
# 修改 nginx.conf 文件，添加SSL配置
```

## 🔧 配置详解

### 1. 数据库配置

```bash
# PostgreSQL配置
POSTGRES_DB=ting_db                    # 数据库名
POSTGRES_USER=ting_user               # 数据库用户
POSTGRES_PASSWORD=ting_password       # 数据库密码
POSTGRES_HOST=localhost               # 数据库主机
POSTGRES_PORT=5432                    # 数据库端口
```

### 2. 缓存配置

```bash
# Redis配置
REDIS_URL=redis://localhost:6379/0    # Redis连接URL
REDIS_HOST=localhost                  # Redis主机
REDIS_PORT=6379                       # Redis端口
REDIS_DB=0                           # Redis数据库
CACHE_DEFAULT_TTL=3600               # 默认缓存时间(秒)
CACHE_LONG_TTL=86400                 # 长期缓存时间(秒)
```

### 3. 微信集成配置

```bash
# 微信公众号配置
WECHAT_APP_ID=your_wechat_app_id                    # 微信应用ID
WECHAT_APP_SECRET=your_wechat_app_secret            # 微信应用密钥
WECHAT_TOKEN=your_wechat_token                      # 微信令牌
WECHAT_ENCODING_AES_KEY=your_encoding_aes_key       # 微信加密密钥

# 微信支付配置
WECHAT_PAY_APPID=your_wechat_pay_appid              # 微信支付应用ID
WECHAT_PAY_MCH_ID=your_wechat_pay_mch_id            # 微信商户号
WECHAT_PAY_API_KEY=your_wechat_pay_api_key          # 微信支付API密钥
```

### 4. 短信服务配置

```bash
# 阿里云短信服务配置
ALIBABA_ACCESS_KEY_ID=your_alibaba_access_key_id     # 阿里云访问密钥ID
ALIBABA_ACCESS_KEY_SECRET=your_alibaba_access_key_secret # 阿里云访问密钥Secret
SMS_SIGN_NAME=您的短信签名                           # 短信签名
SMS_TEMPLATE_CODE=SMS_XXXXXXXXX                     # 短信模板CODE
```

### 5. 文件存储配置

```bash
# 阿里云OSS配置
OSS_ACCESS_KEY_ID=your_oss_access_key_id            # OSS访问密钥ID
OSS_ACCESS_KEY_SECRET=your_oss_access_key_secret    # OSS访问密钥Secret
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com          # OSS端点
OSS_BUCKET_NAME=your_bucket_name                    # OSS存储桶名称
OSS_CDN_DOMAIN=https://your-cdn-domain.com          # CDN域名
```

## 🛠️ 常用命令

### 服务管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
```

### 数据库管理

```bash
# 数据库备份
docker-compose exec postgres pg_dump -U ting_user ting_db > backup.sql

# 数据库恢复
cat backup.sql | docker-compose exec -T postgres psql -U ting_user ting_db

# 进入数据库
docker-compose exec postgres psql -U ting_user -d ting_db
```

### 数据库迁移

```bash
# 生成迁移脚本
docker-compose exec backend alembic revision --autogenerate -m "migration_message"

# 执行迁移
docker-compose exec backend alembic upgrade head

# 回滚迁移
docker-compose exec backend alembic downgrade -1
```

## 🚦 故障排除

### 1. 服务启动失败

```bash
# 检查服务状态
docker-compose ps

# 查看详细日志
docker-compose logs backend
docker-compose logs postgres
docker-compose logs redis
```

### 2. 数据库连接失败

```bash
# 检查数据库是否运行
docker-compose exec postgres pg_isready

# 检查数据库连接
docker-compose exec backend python -c "
import psycopg2
conn = psycopg2.connect(
    host='postgres',
    database='ting_db',
    user='ting_user',
    password='ting_password'
)
print('Database connected successfully')
"
```

### 3. 端口冲突

```bash
# 检查端口占用
netstat -tlnp | grep :8000
netstat -tlnp | grep :3000
netstat -tlnp | grep :5432
```

### 4. 权限问题

```bash
# 检查容器权限
docker-compose exec backend ls -la /app
docker-compose exec backend whoami
```

## 🔒 安全配置

### 1. 生产环境安全建议

- 更改默认的数据库密码
- 使用强密码和密钥
- 配置防火墙规则
- 启用HTTPS
- 定期更新依赖包
- 配置安全头信息

### 2. 敏感信息保护

- 不要将敏感信息提交到代码仓库
- 使用环境变量管理敏感信息
- 定期轮换密钥
- 限制访问权限

## 📊 性能优化

### 1. 数据库优化

```sql
-- 创建索引
CREATE INDEX idx_contents_category ON contents(category);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_points_user_id ON point_transactions(user_id);
```

### 2. 缓存策略

- 配置Redis作为缓存
- 设置合理的缓存策略
- 实现缓存预热
- 监控缓存命中率

### 3. 静态资源优化

- 启用Gzip压缩
- 配置CDN
- 优化图片资源
- 设置合适的缓存头

## 🔄 更新升级

### 1. 拉取最新代码

```bash
# 拉取最新代码
git pull origin main

# 重建服务
docker-compose build
docker-compose up -d
```

### 2. 数据库迁移

```bash
# 执行数据库迁移
docker-compose exec backend alembic upgrade head
```

## 📞 技术支持

如有问题，请参考以下资源：

- **GitHub Issues**: https://github.com/johocn/ting/issues
- **文档**: 项目docs目录
- **邮箱**: support@ting.com

---

**注意**: 生产环境部署前请务必备份数据并充分测试！
