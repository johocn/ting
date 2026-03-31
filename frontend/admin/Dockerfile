FROM node:16-alpine AS builder

WORKDIR /app

# 复制package文件
COPY frontend/admin/package*.json ./
RUN npm ci --only=production

# 复制源码并构建
COPY frontend/admin/ .
RUN npm run build

# 生产环境
FROM nginx:alpine

# 复制构建结果和nginx配置
COPY --from=builder /app/dist /usr/share/nginx/html
COPY frontend/admin/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
