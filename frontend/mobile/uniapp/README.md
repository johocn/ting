# Ting 移动端应用

基于 UniApp 开发的跨平台移动应用，支持 H5、微信小程序等多端运行。

## 🚀 快速开始

### 环境要求

- Node.js 14+
- HBuilderX (可选，用于可视化开发)
- 微信开发者工具 (如需小程序端)

### 安装依赖

```bash
cd frontend/mobile/uniapp
npm install
```

### 开发模式

```bash
# H5 开发
npm run dev:h5

# 微信小程序开发
npm run dev:mp-weixin
```

### 构建生产版本

```bash
# H5 生产构建
npm run build:h5

# 微信小程序生产构建
npm run build:mp-weixin
```

## 📁 项目结构

```
src/
├── pages/              # 页面目录
│   ├── index/         # 首页
│   ├── login/         # 登录页
│   ├── register/      # 注册页
│   ├── learning/      # 学习中心
│   ├── player/        # 播放器
│   ├── points/        # 积分中心
│   ├── channels/      # 渠道管理
│   ├── profile/       # 个人中心
│   ├── profile-edit/  # 编辑资料
│   └── history/       # 学习历史
├── components/         # 组件目录
├── utils/             # 工具函数
│   ├── request.js     # HTTP 请求封装
│   └── api.js         # API 接口定义
├── store/             # 状态管理
├── assets/            # 静态资源
└── App.vue            # 应用入口
```

## 🎨 功能模块

### 已实现功能

- ✅ 用户注册/登录
- ✅ 学习内容浏览
- ✅ 视频/音频播放器
- ✅ 学习进度跟踪
- ✅ 积分查询
- ✅ 渠道管理
- ✅ 个人中心
- ✅ 学习历史记录

### 开发中功能

- ⏳ 积分商城
- ⏳ 每日签到
- ⏳ 渠道创建
- ⏳ 安全设置

## 🔧 配置说明

### API 地址配置

编辑 `src/utils/request.js`:

```javascript
// 生产环境
const BASE_URL = 'http://www.joyogo.com/tingapi';

// 开发环境
// const BASE_URL = 'http://localhost:8000';
```

### 主题色配置

编辑 `src/App.vue` 中的全局样式。

## 📱 多端适配

### H5

- 访问地址：`http://localhost:8080`
- 支持现代浏览器

### 微信小程序

1. 执行 `npm run build:mp-weixin`
2. 用微信开发者工具导入 `dist/dev/mp-weixin` 目录
3. 配置 AppID 并上传

## 🐛 常见问题

### 跨域问题

开发环境如遇跨域问题，可在后端配置 CORS 或使用 nginx 代理。

### 样式兼容性

使用 UniApp 的 rpx 单位进行响应式布局，1rpx = 0.5px (750 屏幕宽度)。

## 📝 开发规范

- 使用 Vue 3 Composition API
- 使用 TypeScript (可选)
- 遵循 UniApp 目录结构规范
- 组件命名使用 PascalCase
- 文件命名使用 kebab-case

## 🚀 部署

### H5 部署

将 `dist/build/h5` 目录内容部署到 Web 服务器。

### 小程序部署

通过微信开发者工具上传代码并提交审核。

## 📄 许可证

MIT License
