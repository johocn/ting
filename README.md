# Ting Learning Platform

## 🚀 项目介绍

基于视频音频学习赚积分的综合性学习平台，支持微信登录、邀请推广、积分商城、线下核销等功能。

## 📋 技术栈

- **后端**: FastAPI + PostgreSQL + Redis
- **管理后台**: Vue3 + Element Plus
- **移动端**: UniApp + 小程序
- **部署**: Docker + Nginx + Docker Compose

## 🏗️ 项目结构

```
ting-platform/
├── backend/           # 后端服务
│   ├── app/          # 应用代码
│   │   ├── api/      # API接口
│   │   ├── models/   # 数据模型
│   │   ├── schemas/  # 数据验证
│   │   ├── core/     # 核心配置
│   │   └── database.py # 数据库配置
│   ├── requirements.txt # Python依赖
│   └── main.py       # 主应用入口
├── frontend/         # 前端项目
│   ├── admin/        # 管理后台
│   └── mobile/       # 移动端
├── docker/           # Docker配置
├── docs/            # 文档
├── scripts/         # 脚本
└── README.md        # 项目说明
```

## 🚀 快速启动

### 开发环境

```bash
# 克隆项目
git clone https://github.com/johocn/ting.git
cd ting

# 启动开发服务
docker-compose up -d

# 访问服务
- 管理后台: http://localhost:3000
- API接口: http://localhost:8000
```

### 生产环境

```bash
# 克隆项目
git clone https://github.com/johocn/ting.git
cd ting

# 构建生产镜像
docker-compose -f docker-compose.prod.yml build

# 启动生产服务
docker-compose -f docker-compose.prod.yml up -d
```

## 📝 API文档

### 认证接口

#### 用户注册
- **POST** `/api/v1/auth/register`
- **参数**:
  ```json
  {
    "username": "用户名",
    "password": "密码",
    "phone": "手机号"
  }
  ```
- **响应**:
  ```json
  {
    "user_id": 1,
    "username": "用户名",
    "token": "JWT令牌"
  }
  ```

#### 用户登录
- **POST** `/api/v1/auth/login`
- **参数**:
  ```json
  {
    "username": "用户名",
    "password": "密码"
  }
  ```
- **响应**:
  ```json
  {
    "user_id": 1,
    "username": "用户名",
    "token": "JWT令牌"
  }
  ```

### 内容接口

#### 获取内容列表
- **GET** `/api/v1/contents`
- **参数**:
  - `skip` (可选): 跳过的数量
  - `limit` (可选): 返回数量
- **响应**:
  ```json
  [
    {
      "id": 1,
      "title": "视频标题",
      "url": "视频URL",
      "duration": 1800,
      "category": "分类",
      "status": true
    }
  ]
  ```

#### 创建内容
- **POST** `/api/v1/contents`
- **认证**: 需要JWT token
- **参数**:
  ```json
  {
    "title": "内容标题",
    "url": "内容URL",
    "duration": 1800,
    "category": "类别",
    "reward_points_per_minute": 5,
    "status": true
  }
  ```

### 积分接口

#### 获取用户积分账户
- **GET** `/api/v1/points/account`
- **认证**: 需要JWT token
- **响应**:
  ```json
  {
    "user_id": 1,
    "total_points": 1000,
    "available_points": 800,
    "frozen_points": 200,
    "expired_points": 0
  }
  ```

#### 获取积分流水
- **GET** `/api/v1/points/transactions`
- **认证**: 需要JWT token
- **参数**:
  - `skip` (可选): 跳过的数量
  - `limit` (可选): 返回数量
- **响应**:
  ```json
  [
    {
      "id": 1,
      "transaction_type": "earn",
      "operation_type": "watch_video",
      "points_change": 50,
      "balance_before": 0,
      "balance_after": 50,
      "description": "观看视频奖励",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
  ```

### 渠道接口

#### 获取我的渠道
- **GET** `/api/v1/channels/my`
- **认证**: 需要JWT token
- **响应**:
  ```json
  [
    {
      "id": 1,
      "name": "渠道名称",
      "code": "邀请码",
      "type_id": 1,
      "parent_channel_id": null,
      "commission_rate": 10.0,
      "invite_link": "邀请链接",
      "stats": {
        "registered_users": 10,
        "active_users": 5
      },
      "created_at": "2024-01-01T00:00:00",
      "is_active": true
    }
  ]
  ```

#### 创建渠道
- **POST** `/api/v1/channels`
- **认证**: 需要JWT token
- **参数**:
  ```json
  {
    "name": "渠道名称",
    "type_id": 1,
    "parent_channel_id": null,
    "commission_rate": 10.0,
    "settings": {}
  }
  ```

### 商城接口

#### 获取商品列表
- **GET** `/api/v1/products`
- **参数**:
  - `category_id` (可选): 分类ID
  - `skip` (可选): 跳过的数量
  - `limit` (可选): 返回数量
- **响应**:
  ```json
  [
    {
      "id": 1,
      "name": "商品名称",
      "description": "商品描述",
      "category_id": 1,
      "points_required": 100,
      "stock_quantity": 100,
      "max_exchange_per_user": 1,
      "is_virtual": false,
      "validity_period_days": 30
    }
  ]
  ```

#### 兌换商品
- **POST** `/api/v1/products/{product_id}/exchange`
- **认证**: 需要JWT token
- **参数**:
  - `quantity` (可选): 兌换数量，默认为1
- **响应**:
  ```json
  {
    "exchange_record_id": 1,
    "exchange_code": "EX123456",
    "product_name": "商品名称",
    "points_deducted": 100,
    "validity_period": "30天",
    "status": "confirmed"
  }
  ```

## 🛠️ 部署指南

详见 `docs/deployment/` 目录

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和PR！
