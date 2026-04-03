#!/bin/bash

echo "=== 初始化Ting学习平台数据库表结构 ==="

# 检查是否已安装psql
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装或未在PATH中"
    exit 1
fi

# 检查PostgreSQL容器是否运行
if ! docker ps | grep -q "ting_postgres"; then
    echo "错误: ting_postgres容器未运行"
    exit 1
fi

echo "连接到PostgreSQL数据库..."

# 创建数据库表结构的SQL命令
docker exec -i ting_postgres psql -U ting_user -d ting_db << 'SQL'
-- 创建channels表（如果不存在）
CREATE TABLE IF NOT EXISTS channel_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS channels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    type_id INTEGER REFERENCES channel_types(id),
    creator_user_id INTEGER,  -- 参考users表
    parent_channel_id INTEGER REFERENCES channels(id),
    level INTEGER DEFAULT 1,
    commission_rate INTEGER DEFAULT 0,
    invite_link TEXT,
    qr_code_url TEXT,
    logo_url TEXT,
    banner_url TEXT,
    settings JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS channel_user_relations (
    id SERIAL PRIMARY KEY,
    channel_id INTEGER REFERENCES channels(id),
    user_id INTEGER,  -- 参考users表
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    invited_by INTEGER,  -- 参考users表
    level INTEGER DEFAULT 1,
    join_source VARCHAR(50) DEFAULT 'direct',
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(channel_id, user_id)
);

CREATE TABLE IF NOT EXISTS channel_statistics (
    id SERIAL PRIMARY KEY,
    channel_id INTEGER REFERENCES channels(id),
    date DATE DEFAULT CURRENT_DATE,
    registered_users INTEGER DEFAULT 0,
    active_users INTEGER DEFAULT 0,
    earned_points INTEGER DEFAULT 0,
    spent_points INTEGER DEFAULT 0,
    exchange_count INTEGER DEFAULT 0,
    verification_count INTEGER DEFAULT 0,
    withdrawal_amount INTEGER DEFAULT 0,
    withdrawal_count INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(channel_id, date)
);

CREATE TABLE IF NOT EXISTS channel_permissions (
    id SERIAL PRIMARY KEY,
    channel_id INTEGER REFERENCES channels(id),
    permission_code VARCHAR(100) NOT NULL,
    permission_name VARCHAR(200) NOT NULL,
    is_allowed BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS channel_point_configs (
    id SERIAL PRIMARY KEY,
    channel_id INTEGER REFERENCES channels(id),
    config_type VARCHAR(50) NOT NULL,
    multiplier INTEGER DEFAULT 100,
    fixed_bonus INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS channel_hierarchy (
    id SERIAL PRIMARY KEY,
    channel_id INTEGER REFERENCES channels(id),
    parent_id INTEGER REFERENCES channels(id),
    level INTEGER NOT NULL,
    path VARCHAR(500),
    depth INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS channel_invitation_records (
    id SERIAL PRIMARY KEY,
    inviter_user_id INTEGER,  -- 参考users表
    invitee_user_id INTEGER,  -- 参考users表
    channel_id INTEGER REFERENCES channels(id),
    invitation_code VARCHAR(50),
    invite_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    registration_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    ip_address VARCHAR(45),
    user_agent TEXT
);

-- 创建更新时间触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为需要自动更新updated_at的表创建触发器
DROP TRIGGER IF EXISTS update_channels_updated_at ON channels;
CREATE TRIGGER update_channels_updated_at 
    BEFORE UPDATE ON channels 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_channel_statistics_updated_at ON channel_statistics;
CREATE TRIGGER update_channel_statistics_updated_at 
    BEFORE UPDATE ON channel_statistics 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 创建索引优化查询
CREATE INDEX IF NOT EXISTS idx_channels_code ON channels(code);
CREATE INDEX IF NOT EXISTS idx_channels_type_id ON channels(type_id);
CREATE INDEX IF NOT EXISTS idx_channels_creator_user_id ON channels(creator_user_id);
CREATE INDEX IF NOT EXISTS idx_channel_user_relations_user_id ON channel_user_relations(user_id);
CREATE INDEX IF NOT EXISTS idx_channel_statistics_date ON channel_statistics(date);
CREATE INDEX IF NOT EXISTS idx_channel_invitation_records_status ON channel_invitation_records(status);

-- 验证表创建
SELECT 'Tables created successfully' AS status;
SQL

if [ $? -eq 0 ]; then
    echo "✓ Ting学习平台数据库表结构初始化完成"
else
    echo "✗ 数据库表结构初始化失败"
    exit 1
fi

echo "=== 数据库初始化完成 ==="