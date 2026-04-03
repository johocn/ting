FROM node:18-alpine

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 安装依赖
RUN npm install --legacy-peer-deps

# 复制源代码
COPY . .

# 构建应用
RUN npm run build:h5

# 安装serve以提供静态文件服务
RUN npm install -g serve

# 暴露端口
EXPOSE 3001

# 启动服务
CMD ["serve", "-s", "dist/build/h5", "-l", "3001"]