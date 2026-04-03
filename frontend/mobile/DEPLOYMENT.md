# Ting 移动端部署指南

## 生产环境部署

### 1. H5 部署

#### 构建生产版本

```bash
cd frontend/mobile/uniapp
npm install
npm run build:h5
```

#### Nginx 配置

```nginx
server {
    listen 80;
    server_name m.joyogo.com;  # 移动端域名
    
    root /var/www/ting-mobile;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # API 代理
    location /tingapi {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # CORS 配置
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS';
        add_header Access-Control-Allow-Headers 'Content-Type, Authorization';
        
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }
}
```

#### 部署步骤

```bash
# 1. 上传构建文件
scp -r dist/build/h5/* user@server:/var/www/ting-mobile

# 2. 配置 Nginx
sudo nano /etc/nginx/sites-available/ting-mobile
sudo ln -s /etc/nginx/sites-available/ting-mobile /etc/nginx/sites-enabled/

# 3. 重启 Nginx
sudo nginx -t
sudo systemctl restart nginx

# 4. 配置 SSL (推荐)
sudo certbot --nginx -d m.joyogo.com
```

### 2. 微信小程序部署

#### 构建小程序

```bash
npm run build:mp-weixin
```

#### 上传步骤

1. 打开微信开发者工具
2. 导入项目：选择 `dist/build/mp-weixin` 目录
3. 配置 AppID (在 `project.config.json` 中)
4. 点击"上传"按钮
5. 登录微信公众平台提交审核

#### 小程序配置

编辑 `manifest.json`:

```json
"mp-weixin": {
  "appid": "your-wechat-appid",
  "setting": {
    "urlCheck": true,
    "es6": true,
    "postcss": true,
    "minified": true
  }
}
```

### 3. API 地址配置

#### 生产环境

编辑 `src/utils/request.js`:

```javascript
const BASE_URL = 'http://www.joyogo.com/tingapi';
```

#### 测试环境

```javascript
const BASE_URL = 'http://test-api.joyogo.com';
```

#### 开发环境

```javascript
const BASE_URL = 'http://localhost:8000';
```

### 4. 性能优化

#### 代码分割

在 `vite.config.ts` 中配置:

```typescript
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue'],
          uni: ['@dcloudio/uni-app']
        }
      }
    }
  }
}
```

#### 图片优化

- 使用 WebP 格式
- 压缩图片资源
- 使用 CDN 加速

#### 缓存策略

Nginx 缓存配置:

```nginx
# 静态资源缓存
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}

# HTML 不缓存
location ~* \.html$ {
    expires -1;
    add_header Cache-Control "no-cache, no-store, must-revalidate";
}
```

### 5. 监控与日志

#### 错误监控

建议集成 Sentry 或其他错误监控服务。

#### 访问日志

Nginx 日志配置:

```nginx
access_log /var/log/nginx/ting-mobile-access.log;
error_log /var/log/nginx/ting-mobile-error.log;
```

### 6. 安全配置

#### HTTPS 强制跳转

```nginx
server {
    listen 80;
    server_name m.joyogo.com;
    return 301 https://$server_name$request_uri;
}
```

#### 安全头信息

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
```

## 测试清单

部署前请确认:

- [ ] API 地址配置正确
- [ ] 所有页面功能正常
- [ ] 登录/注册流程通畅
- [ ] 视频播放正常
- [ ] 积分显示正确
- [ ] 移动端适配良好
- [ ] SSL 证书有效
- [ ] 错误监控已配置

## 回滚方案

如遇问题需要回滚:

```bash
# 备份当前版本
cp -r /var/www/ting-mobile /var/www/ting-mobile.backup.$(date +%Y%m%d)

# 恢复旧版本
cp -r /var/www/ting-mobile.backup.20260402 /var/www/ting-mobile

# 重启 Nginx
sudo systemctl restart nginx
```

## 联系支持

如有问题，请联系开发团队或查看项目文档。
