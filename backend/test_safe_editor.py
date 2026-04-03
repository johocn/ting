#!/usr/bin/env python3
"""
测试安全文件编辑器
"""

import sys
import os
sys.path.append('/home/admin/.openclaw/workspace/ting/backend')

from app.utils.file_editor import SafeFileEditor
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_safe_editor():
    """测试安全编辑器功能"""
    filepath = "/home/admin/.openclaw/workspace/ting/backend/app/models/channels.py"
    
    print("测试安全文件编辑器...")
    
    # 创建编辑器实例
    editor = SafeFileEditor(filepath)
    
    print(f"文件路径: {filepath}")
    print(f"使用的策略: {editor.strategy}")
    print(f"配置加载成功: {bool(editor.config)}")
    
    # 测试读取
    print("\n测试读取文件...")
    content = editor.read_with_retry()
    if content:
        print(f"✓ 成功读取 {len(content)} 个字符")
    else:
        print("✗ 读取失败")
        return False
    
    # 测试验证完整性
    print("\n测试完整性验证...")
    if editor.validate_file_integrity():
        print("✓ 完整性验证通过")
    else:
        print("✗ 完整性验证失败")
        return False
    
    # 测试简单的替换操作（不实际修改文件，只是测试流程）
    print("\n测试替换操作...")
    test_content = content.replace(
        'qr_code_url = Column(Text)  # 二维码链接',
        'qr_code_url = Column(Text)  # 二维码链接\n    logo_url = Column(Text)  # Logo链接'
    )
    
    # 验证保护规则
    if editor._check_protection_rules(test_content):
        print("✓ 保护规则检查通过")
    else:
        print("✗ 保护规则检查失败")
        return False
    
    print("\n所有测试通过！")
    return True

def quick_edit_test():
    """快速编辑测试"""
    filepath = "/home/admin/.openclaw/workspace/ting/backend/app/models/channels.py"
    
    print("\n执行快速编辑测试...")
    
    # 创建编辑器
    editor = SafeFileEditor(filepath)
    
    # 尝试一个简单的替换操作
    success = editor.safe_replace_content(
        'qr_code_url = Column(Text)  # 二维码链接',
        'qr_code_url = Column(Text)  # 二维码链接\n    logo_url = Column(Text)  # Logo链接',
        backup=True
    )
    
    if success:
        print("✓ 编辑操作成功完成")
        return True
    else:
        print("✗ 编辑操作失败")
        return False

if __name__ == "__main__":
    print("安全文件编辑器测试")
    print("=" * 50)
    
    success1 = test_safe_editor()
    success2 = quick_edit_test() if success1 else False
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("所有测试成功完成！")
        print("\n安全编辑策略已准备就绪，可以有效减少编辑错误。")
    else:
        print("测试失败！")