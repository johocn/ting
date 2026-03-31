#!/bin/bash

# Ting Learning Platform 部署脚本
# 用于生产环境的一键部署

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查必要工具
check_prerequisites() {
    log_info "检查部署环境..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    log_success "环境检查完成"
}

# 检查配置文件
check_config_files() {
    log_info "检查配置文件..."
    
    if [ ! -f ".env" ]; then
        log_warn ".env 文件不存在，使用示例配置文件"
        if [ -f ".env.example" ]; then
            cp .env.example .env
            log_info "已复制 .env.example 到 .env，请修改配置参数"
            exit 1
        else
            log_error ".env.example 文件也不存在"
            exit 1
        fi
    fi
    
    # 验证必要的环境变量
    required_vars=(
        "POSTGRES_DB"
        "POSTGRES_USER" 
        "POSTGRES_PASSWORD"
        "SECRET_KEY"
    )
    
    missing_vars=()
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        log_error "缺少必要的环境变量: ${missing_vars[*]}"
        log_info "请检查 .env 文件并设置必要的配置参数"
        exit 1
    fi
    
    log_success "配置文件检查完成"
}

# 构建镜像
build_images() {
    log_info "开始构建 Docker 镜像..."
    
    # 构建后端镜像
    log_info "构建后端服务镜像..."
    docker-compose -f docker-compose.prod.yml build backend
    
    # 构建前端镜像
    log_info "构建前端服务镜像..."
    docker-compose -f docker-compose.prod.yml build admin-frontend
    
    log_success "Docker 镜像构建完成"
}

# 数据库迁移
run_migrations() {
    log_info "执行数据库迁移..."
    
    # 启动数据库服务
    docker-compose -f docker-compose.prod.yml up -d postgres
    
    # 等待数据库就绪
    sleep 10
    
    # 执行迁移
    docker-compose -f docker-compose.prod.yml run --rm backend alembic upgrade head
    
    log_success "数据库迁移完成"
}

# 启动服务
start_services() {
    log_info "启动服务..."
    
    # 停止现有服务
    docker-compose -f docker-compose.prod.yml down || true
    
    # 启动所有服务
    docker-compose -f docker-compose.prod.yml up -d
    
    log_success "服务启动完成"
}

# 健康检查
health_check() {
    log_info "执行健康检查..."
    
    # 检查后端服务
    for i in {1..30}; do
        if curl -f http://localhost:8000/health > /dev/null 2>&1; then
            log_success "后端服务健康检查通过"
            break
        fi
        log_info "等待后端服务就绪... ($i/30)"
        sleep 10
    done
    
    if [ $i -eq 30 ]; then
        log_error "后端服务启动失败"
        exit 1
    fi
    
    # 检查前端服务
    for i in {1..10}; do
        if curl -f http://localhost:3000 > /dev/null 2>&1; then
            log_success "前端服务健康检查通过"
            break
        fi
        log_info "等待前端服务就绪... ($i/10)"
        sleep 5
    done
    
    log_success "所有服务健康检查通过"
}

# 显示部署信息
show_deployment_info() {
    log_info "=== 部署完成 ==="
    echo "管理后台: http://$(hostname):3000"
    echo "API接口: http://$(hostname):8000"
    echo "数据库: $(hostname):5432"
    echo "Redis: $(hostname):6379"
    echo ""
    log_success "Ting Learning Platform 部署成功！"
}

# 主函数
main() {
    log_info "开始部署 Ting Learning Platform..."
    
    check_prerequisites
    check_config_files
    build_images
    run_migrations
    start_services
    health_check
    show_deployment_info
    
    log_success "部署完成！"
}

# 执行主函数
main "$@"
