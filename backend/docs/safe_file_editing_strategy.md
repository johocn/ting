# 安全文件编辑策略指南

## 概述

为了减少文件编辑错误（如 "⚠️ 📝 Edit: in ~/.openclaw/workspace/ting/backend/app/models/channels.py (183 chars) failed"），我们实现了安全的分段编辑策略。

## 核心组件

### 1. SafeFileEditor 类
- 提供多种安全编辑方法
- 支持重试机制和指数退避
- 自动备份和文件完整性验证

### 2. 配置驱动
- YAML配置文件控制编辑行为
- 支持不同文件类型和路径的差异化策略
- 可自定义重试次数、延迟时间等参数

### 3. 保护机制
- 文件大小变化限制
- 危险模式检测
- 语法验证（Python、JSON、YAML）
- 空内容写入保护

## 使用方法

### 基本使用
```python
from app.utils.file_editor import SafeFileEditor

# 创建编辑器实例
editor = SafeFileEditor("/path/to/your/file.py")

# 安全替换内容
success = editor.safe_replace_content(
    old_text="old content",
    new_text="new content",
    backup=True
)

# 在指定行插入
success = editor.safe_insert_at_line(
    line_number=10,
    text="new line content",
    backup=True
)

# 正则表达式替换
success = editor.safe_replace_regex(
    pattern=r"pattern",
    replacement="replacement",
    backup=True
)
```

### 批量操作
```python
from app.utils.file_editor import segment_edit_file

operations = [
    ('replace', {
        'old_text': 'old content',
        'new_text': 'new content'
    }),
    ('insert_at_line', {
        'line_number': 10,
        'text': 'new line'
    })
]

success = segment_edit_file("/path/to/file.py", operations)
```

## 策略配置

配置文件位于 `config/file_edit_config.yaml`，包含：

- **GENERAL**: 通用设置（备份数量、重试次数等）
- **EDIT_STRATEGIES**: 不同场景的编辑策略
- **FILE_TYPES**: 文件类型的差异化处理
- **CRITICAL_PATHS**: 关键路径识别
- **PROTECTION_RULES**: 保护规则

## 优势

1. **减少编辑失败**: 通过重试机制和文件锁定处理
2. **数据安全**: 自动备份和完整性验证
3. **灵活配置**: 支持不同场景的定制化策略
4. **错误恢复**: 提供备份文件便于回滚
5. **语法保护**: 防止引入语法错误

## 最佳实践

1. 在编辑重要文件前先进行备份
2. 使用适当的重试策略
3. 验证编辑后的文件完整性
4. 定期清理旧备份文件
5. 监控编辑操作的日志

这套策略能够显著减少文件编辑错误，提高开发效率和代码安全性。