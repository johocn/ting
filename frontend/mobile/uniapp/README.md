# Ting学习平台移动端 (uni-app)

基于uni-app开发的跨平台移动应用，支持H5和微信小程序。

## 项目结构

```
src/
├── App.vue           # 应用入口组件
├── main.ts           # 应用入口文件
├── pages/            # 页面文件
├── components/       # 组件文件
├── assets/           # 静态资源
├── router/           # 路由配置
├── stores/           # 状态管理
└── views/            # 视图组件
```

## 安装依赖

```bash
npm install
```

## 开发运行

```bash
# 开发模式运行H5
npm run dev:h5

# 开发模式运行微信小程序
npm run dev:mp-weixin

# 构建H5版本
npm run build:h5

# 构建微信小程序
npm run build:mp-weixin
```

## 环境配置

此项目与Ting后端服务集成，API请求通过代理转发到后端服务。

## 功能模块

- 学习模块：支持视频音频学习
- 积分系统：学习赚取积分
- 用户中心：个人信息管理
- 邀请推广：渠道管理
- 积分商城：兑换商品