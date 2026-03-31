# API 文档

## 📖 概述

Ting Learning Platform API 提供了完整的学习、积分、商城、渠道管理等功能的接口。

## 🔐 认证

所有需要认证的接口都需要在请求头中包含JWT token：
```
Authorization: Bearer <jwt_token>
```

## 📊 通用响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 📁 接口分类

### 1. 认证接口

#### 用户注册
- **URL**: `POST /api/v1/auth/register`
- **描述**: 用户注册接口
- **请求体**:
```json
{
  "username": "string",
  "password": "string",
  "phone": "string"
}
```
- **响应**:
```json
{
  "user_id": 1,
  "username": "string",
  "token": "string"
}
```

#### 用户登录
- **URL**: `POST /api/v1/auth/login`
- **描述**: 用户登录接口
- **请求体**:
```json
{
  "username": "string",
  "password": "string"
}
```
- **响应**:
```json
{
  "user_id": 1,
  "username": "string",
  "token": "string"
}
```

### 2. 用户接口

#### 获取用户资料
- **URL**: `GET /api/v1/users/profile`
- **认证**: 需要JWT token
- **描述**: 获取当前用户资料
- **响应**:
```json
{
  "id": 1,
  "username": "string",
  "phone": "string",
  "email": "string",
  "integral": 100,
  "level": 1,
  "is_member": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 更新用户资料
- **URL**: `PUT /api/v1/users/profile`
- **认证**: 需要JWT token
- **描述**: 更新当前用户资料
- **请求体**:
```json
{
  "username": "string",
  "phone": "string",
  "email": "string"
}
```

### 3. 内容接口

#### 获取内容列表
- **URL**: `GET /api/v1/contents`
- **认证**: 可选
- **参数**:
  - `skip` (int): 跳过的数量
  - `limit` (int): 返回数量
  - `category` (string): 分类
  - `status` (bool): 状态
- **描述**: 获取内容列表
- **响应**:
```json
{
  "items": [
    {
      "id": 1,
      "title": "string",
      "url": "string",
      "duration": 1800,
      "category": "string",
      "reward_points_per_minute": 5,
      "status": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 100,
  "skip": 0,
  "limit": 10
}
```

#### 创建内容
- **URL**: `POST /api/v1/contents`
- **认证**: 需要JWT token
- **描述**: 创建新内容
- **请求体**:
```json
{
  "title": "string",
  "url": "string",
  "duration": 1800,
  "category": "string",
  "reward_points_per_minute": 5,
  "status": true
}
```

### 4. 积分接口

#### 获取积分账户
- **URL**: `GET /api/v1/points/account`
- **认证**: 需要JWT token
- **描述**: 获取用户积分账户信息
- **响应**:
```json
{
  "user_id": 1,
  "total_points": 1000,
  "available_points": 800,
  "frozen_points": 200,
  "expired_points": 0,
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 获取积分流水
- **URL**: `GET /api/v1/points/transactions`
- **认证**: 需要JWT token
- **参数**:
  - `skip` (int): 跳过的数量
  - `limit` (int): 返回数量
  - `type` (string): 交易类型
- **描述**: 获取积分流水记录
- **响应**:
```json
{
  "items": [
    {
      "id": 1,
      "transaction_type": "earn",
      "operation_type": "watch_video",
      "points_change": 50,
      "balance_before": 0,
      "balance_after": 50,
      "description": "观看视频奖励",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 100,
  "skip": 0,
  "limit": 10
}
```

### 5. 渠道接口

#### 获取我的渠道
- **URL**: `GET /api/v1/channels/my`
- **认证**: 需要JWT token
- **描述**: 获取用户创建的渠道列表
- **响应**:
```json
{
  "channels": [
    {
      "id": 1,
      "name": "渠道名称",
      "code": "邀请码",
      "type_id": 1,
      "commission_rate": 10.0,
      "invite_link": "邀请链接",
      "stats": {
        "registered_users": 10,
        "active_users": 5
      },
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### 获取渠道统计
- **URL**: `GET /api/v1/channels/{channel_id}/statistics`
- **认证**: 需要JWT token
- **描述**: 获取渠道统计数据
- **参数**:
  - `start_date` (string): 开始日期
  - `end_date` (string): 结束日期
- **响应**:
```json
{
  "channel_id": 1,
  "period": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  },
  "total_registered": 10,
  "total_active": 5,
  "total_earned_points": 1000,
  "total_spent_points": 500,
  "daily_stats": [
    {
      "date": "2024-01-01",
      "registered_users": 1,
      "active_users": 1,
      "earned_points": 100,
      "spent_points": 50
    }
  ]
}
```

### 6. 商城接口

#### 获取商品列表
- **URL**: `GET /api/v1/products`
- **认证**: 可选
- **参数**:
  - `category_id` (int): 分类ID
  - `skip` (int): 跳过的数量
  - `limit` (int): 返回数量
- **描述**: 获取商品列表
- **响应**:
```json
{
  "items": [
    {
      "id": 1,
      "name": "商品名称",
      "description": "商品描述",
      "category_id": 1,
      "points_required": 100,
      "stock_quantity": 100,
      "is_virtual": false,
      "validity_period_days": 30,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 100,
  "skip": 0,
  "limit": 10
}
```

#### 兌换商品
- **URL**: `POST /api/v1/products/{product_id}/exchange`
- **认证**: 需要JWT token
- **描述**: 兌换商品
- **参数**:
  - `quantity` (int): 兌换数量
- **响应**:
```json
{
  "exchange_record_id": 1,
  "exchange_code": "EX123456",
  "product_name": "商品名称",
  "points_deducted": 100,
  "quantity": 1,
  "validity_start_date": "2024-01-01",
  "validity_end_date": "2024-01-31",
  "status": "confirmed"
}
```

### 7. 核销接口

#### 获取门店信息
- **URL**: `GET /api/v1/verification/store-info`
- **认证**: 需要JWT token
- **描述**: 获取门店员工的门店信息
- **响应**:
```json
{
  "store": {
    "id": 1,
    "name": "门店名称",
    "address": "门店地址",
    "phone": "门店电话"
  }
}
```

#### 确认核销
- **URL**: `POST /api/v1/verification/confirm`
- **认证**: 需要JWT token
- **描述**: 确认兑换记录的核销
- **请求体**:
```json
{
  "exchange_record_id": 1,
  "verification_code": "VER20240101001"
}
```
- **响应**:
```json
{
  "status": "success",
  "message": "核销成功"
}
```

## 📞 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 📋 请求示例

### Python (requests)
```python
import requests

# 设置基础URL和认证头
base_url = "http://localhost:8000/api/v1"
headers = {
    "Authorization": "Bearer your_jwt_token_here",
    "Content-Type": "application/json"
}

# 获取用户资料
response = requests.get(f"{base_url}/users/profile", headers=headers)
print(response.json())
```

### JavaScript (fetch)
```javascript
const token = 'your_jwt_token_here';
const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
};

// 获取内容列表
fetch('http://localhost:8000/api/v1/contents', {
    method: 'GET',
    headers: headers
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🛠️ SDK

详细的SDK使用说明请参见各语言的客户端库文档。

## 📞 支持

如有疑问请联系技术支持。
