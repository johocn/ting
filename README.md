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
└── docs/            # 文档
```

## 🚀 快速启动

```bash
# 克隆项目
git clone https://github.com/johocn/ting.git
cd ting

# 启动服务
docker-compose up -d

# 访问服务
- 管理后台: http://localhost:3000
- API接口: http://localhost:8000
```

## 📝 API文档

API文档请参考 `docs/api/` 目录

## 🛠️ 部署

详细部署文档请参考 `docs/deploy/` 目录

## 🤝 贡献

欢迎提交Issue和PR！

## 📄 许可证

MIT License
