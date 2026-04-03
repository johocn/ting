FROM node:16-alpine AS builder

WORKDIR /app

# 复制package文件
COPY package*.json ./
RUN npm install --legacy-peer-deps

# 复制源码并构建
COPY . .
RUN npm run build

# 生产环境
FROM nginx:alpine

# 复制构建结果
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
