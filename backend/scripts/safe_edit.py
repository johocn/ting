#!/usr/bin/env python3
"""
快速安全编辑脚本
用于安全地编辑文件，减少编辑错误
"""

import sys
import os
import argparse

# 添加项目路径
sys.path.append('/home/admin/.openclaw/workspace/ting/backend')

from app.utils.file_editor import SafeFileEditor

def main():
    parser = argparse.ArgumentParser(description='安全文件编辑工具')
    parser.add_argument('filepath', help='要编辑的文件路径')
    parser.add_argument('--operation', '-o', choices=['replace', 'insert', 'regex', 'append'], 
                       required=True, help='编辑操作类型')
    parser.add_argument('--old-text', help='要替换的原文（replace操作）')
    parser.add_argument('--new-text', help='新文本')
    parser.add_argument('--line-number', type=int, help='行号（insert操作）')
    parser.add_argument('--pattern', help='正则表达式（regex操作）')
    parser.add_argument('--backup', action='store_true', default=True, help='是否创建备份')
    
    args = parser.parse_args()
    
    # 创建编辑器
    editor = SafeFileEditor(args.filepath)
    
    success = False
    
    if args.operation == 'replace':
        if not args.old_text or not args.new_text:
            print("错误: replace操作需要--old-text和--new-text参数")
            sys.exit(1)
        success = editor.safe_replace_content(args.old_text, args.new_text, args.backup)
        
    elif args.operation == 'insert':
        if args.line_number is None or not args.new_text:
            print("错误: insert操作需要--line-number和--new-text参数")
            sys.exit(1)
        success = editor.safe_insert_at_line(args.line_number, args.new_text, args.backup)
        
    elif args.operation == 'regex':
        if not args.pattern or not args.new_text:
            print("错误: regex操作需要--pattern和--new-text参数")
            sys.exit(1)
        success = editor.safe_replace_regex(args.pattern, args.new_text, args.backup)
        
    elif args.operation == 'append':
        if not args.new_text:
            print("错误: append操作需要--new-text参数")
            sys.exit(1)
        success = editor.safe_append_content(args.new_text, args.backup)
    
    if success:
        print(f"✓ {args.operation} 操作成功完成")
        if args.backup:
            print("✓ 已创建备份文件")
    else:
        print(f"✗ {args.operation} 操作失败")
        sys.exit(1)

if __name__ == "__main__":
    main()