#!/usr/bin/env python3
"""
安全编辑示例脚本 - 演示如何使用 SafeFileEditor 安全地编辑 channels.py 文件
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.file_editor import SafeFileEditor, segment_edit_file
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def demonstrate_safe_edits():
    """演示各种安全编辑操作"""
    filepath = "/home/admin/.openclaw/workspace/ting/backend/app/models/channels.py"
    
    print("=== 安全文件编辑演示 ===")
    
    # 创建编辑器实例
    editor = SafeFileEditor(filepath)
    
    # 1. 验证文件完整性
    print("\n1. 验证文件完整性...")
    if editor.validate_file_integrity():
        print("✓ 文件完整性验证通过")
    else:
        print("✗ 文件完整性验证失败")
        return False
    
    # 2. 读取文件内容（带重试）
    print("\n2. 读取文件内容...")
    content = editor.read_with_retry()
    if content is None:
        print("✗ 无法读取文件")
        return False
    print(f"✓ 成功读取文件，共 {len(content)} 个字符")
    
    # 3. 演示不同的编辑操作
    
    # 示例1: 安全替换（添加新字段）
    print("\n3. 演示安全替换操作...")
    success = editor.safe_replace_content(
        'qr_code_url = Column(Text)  # 二维码链接',
        'qr_code_url = Column(Text)  # 二维码链接\n    logo_url = Column(Text)  # Logo链接',
        backup=True
    )
    if success:
        print("✓ 替换操作成功")
    else:
        print("✗ 替换操作失败")
    
    # 示例2: 在指定行插入内容
    print("\n4. 演示行插入操作...")
    # 找到 Channel 类定义的位置
    lines = content.split('\n')
    channel_class_line = -1
    for i, line in enumerate(lines):
        if 'class Channel(Base):' in line:
            channel_class_line = i + 1  # 在类定义后插入
            break
    
    if channel_class_line != -1:
        success = editor.safe_insert_at_line(
            channel_class_line,
            "    # 新增字段示例",
            backup=False  # 不重复备份
        )
        if success:
            print("✓ 行插入操作成功")
        else:
            print("✗ 行插入操作失败")
    
    # 示例3: 正则表达式替换
    print("\n5. 演示正则替换操作...")
    success = editor.safe_replace_regex(
        r'commission_rate = Column\(Integer, default=0\)  # 佣金比例',
        'commission_rate = Column(Integer, default=0)  # 佣金比例\n    max_commission_rate = Column(Integer, default=100)  # 最大佣金比例',
        backup=False
    )
    if success:
        print("✓ 正则替换操作成功")
    else:
        print("✗ 正则替换操作失败")
    
    # 6. 最终验证
    print("\n6. 最终文件验证...")
    if editor.validate_file_integrity():
        print("✓ 最终文件完整性验证通过")
        return True
    else:
        print("✗ 最终文件完整性验证失败")
        return False


def perform_specific_edit():
    """执行特定的编辑操作"""
    filepath = "/home/admin/.openclaw/workspace/ting/backend/app/models/channels.py"
    
    print("=== 执行特定编辑操作 ===")
    
    # 定义要执行的操作序列
    operations = [
        # 1. 为 Channel 模型添加新字段
        ('replace', {
            'old_text': 'qr_code_url = Column(Text)  # 二维码链接',
            'new_text': '''qr_code_url = Column(Text)  # 二维码链接
    logo_url = Column(Text)  # Logo链接
    banner_url = Column(Text)  # 横幅图片链接''',
            'backup': True
        }),
        
        # 2. 为 ChannelStatistics 模型添加新字段
        ('replace', {
            'old_text': 'verification_count = Column(Integer, default=0)  # 核销次数',
            'new_text': '''verification_count = Column(Integer, default=0)  # 核销次数
    withdrawal_amount = Column(Integer, default=0)  # 提现金额
    withdrawal_count = Column(Integer, default=0)  # 提现次数''',
            'backup': False
        }),
        
        # 3. 为 ChannelUserRelation 模型添加新字段
        ('replace', {
            'old_text': 'level = Column(Integer, default=1)  # 用户在渠道中的层级',
            'new_text': '''level = Column(Integer, default=1)  # 用户在渠道中的层级
    join_source = Column(String(50), default='direct')  # 加入来源：direct, invite, scan_qr等''',
            'backup': False
        })
    ]
    
    success = segment_edit_file(filepath, operations)
    
    if success:
        print("✓ 所有编辑操作成功完成")
        
        # 验证最终结果
        editor = SafeFileEditor(filepath)
        if editor.validate_file_integrity():
            print("✓ 最终文件完整性验证通过")
            return True
        else:
            print("✗ 最终文件完整性验证失败")
            return False
    else:
        print("✗ 编辑操作失败")
        return False


def rollback_if_needed():
    """如有需要，执行回滚操作"""
    filepath = "/home/admin/.openclaw/workspace/ting/backend/app/models/channels.py"
    
    print("\n=== 回滚操作示例 ===")
    print("注意：这里只是演示如何找到最近的备份文件")
    
    import glob
    import os
    
    backup_pattern = f"{filepath}.backup.*"
    backups = glob.glob(backup_pattern)
    
    if backups:
        # 按修改时间排序，最新的在前
        backups.sort(key=os.path.getmtime, reverse=True)
        print(f"找到 {len(backups)} 个备份文件:")
        for backup in backups[:5]:  # 显示最新的5个
            mtime = os.path.getmtime(backup)
            import datetime
            time_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  - {backup} ({time_str})")
        
        print("\n如果需要回滚，可以使用:")
        print(f"  cp '{backups[0]}' '{filepath}'")
    else:
        print("未找到备份文件")


def main():
    """主函数"""
    print("安全文件编辑策略演示")
    print("=" * 50)
    
    # 执行演示
    success = perform_specific_edit()
    
    if success:
        print("\n" + "=" * 50)
        print("编辑操作完成！")
        
        # 显示备份信息
        rollback_if_needed()
    else:
        print("\n" + "=" * 50)
        print("编辑操作失败！")
        
        # 显示可用备份
        rollback_if_needed()
    
    return success


if __name__ == "__main__":
    main()