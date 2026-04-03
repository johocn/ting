# Ting Learning Platform - Uniapp Frontend

这是Ting学习平台的Uniapp前端项目，为学习者提供移动端体验。

## 项目结构

```
uniapp/
├── pages/              # 页面文件
│   ├── index/          # 首页
│   ├── about/          # 关于我们
│   ├── user/           # 用户中心
│   ├── learning/       # 学习中心
│   ├── content/        # 内管理
│   ├── quiz/           # 答题练习
│   ├── points/         # 积分中心
│   └── mall/           # 积分商城
├── static/             # 静态资源
├── components/         # 公共组件
├── utils/              # 工具函数
├── uni_modules/        # uni_modules插件
├── App.vue             # 应用入口
├── main.js             # 应用初始化
├── manifest.json       # 应用配置
├── pages.json          # 页面路由配置
├── uni.scss            # 全局样式变量
└── package.json        # 项目依赖
```

## 功能模块

- 首页：平台介绍和导航
- 学习中心：观看视频、音频内容，参与答题
- 内管理：学习资料和课程管理
- 答题练习：随堂测验和练习
- 积分中心：积分获取和记录
- 积分商城：积分兑换礼品
- 用户中心：个人信息和设置

## 技术栈

- 框架：uni-app (Vue 3)
- 语言：Vue.js, JavaScript/ES6
- 构建工具：npm
- 样式：SASS/SCSS

## 运行方式

```bash
# 安装依赖
npm install

# 开发模式运行
npm run dev

# 构建发布版本
npm run build
```

## 目标平台

- H5网页版
- 微信小程序
- App（Android/iOS）
- 其他小程序平台