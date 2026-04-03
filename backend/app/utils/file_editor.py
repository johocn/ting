import tempfile
import shutil
import os
import time
import logging
from typing import List, Tuple, Optional
import re
import yaml
import json

class SafeFileEditor:
    """
    安全文件编辑器 - 实现分段编辑策略，减少编辑错误
    """
    
    def __init__(self, filepath: str, config_path: str = None, backup_count: int = 3):
        self.filepath = filepath
        self.backup_count = backup_count
        self.logger = logging.getLogger(__name__)
        
        # 加载配置
        self.config = self._load_config(config_path)
        
        # 根据文件类型和路径确定策略
        self.strategy = self._determine_strategy()
    
    def _load_config(self, config_path: str = None) -> dict:
        """加载配置文件"""
        if config_path is None:
            config_path = "/home/admin/.openclaw/workspace/ting/backend/config/file_edit_config.yaml"
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                self.logger.warning(f"无法加载配置文件 {config_path}: {e}")
                return self._get_default_config()
        else:
            self.logger.info(f"配置文件不存在，使用默认配置: {config_path}")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """获取默认配置"""
        return {
            'GENERAL': {
                'BACKUP_COUNT': 3,
                'MAX_RETRIES': 3,
                'INITIAL_DELAY': 0.1,
                'VERBOSE_LOGGING': False
            },
            'EDIT_STRATEGIES': {
                'DEFAULT': {
                    'backup': True,
                    'max_retries': 3,
                    'delay': 0.1
                }
            },
            'FILE_TYPES': {
                'python': {
                    'extensions': ['.py'],
                    'strategy': 'DEFAULT',
                    'syntax_check': True
                }
            },
            'CRITICAL_PATHS': [],
            'PROTECTION_RULES': {
                'SIZE_CHANGE_LIMIT': 3.0,
                'PREVENT_EMPTY_WRITE': True,
                'DANGEROUS_PATTERNS': []
            }
        }
    
    def _determine_strategy(self) -> dict:
        """根据文件类型和路径确定编辑策略"""
        # 获取文件扩展名
        _, ext = os.path.splitext(self.filepath)
        ext = ext.lower()
        
        # 检查是否为关键路径
        is_critical_path = any(self._matches_path_pattern(self.filepath, pattern) 
                              for pattern in self.config.get('CRITICAL_PATHS', []))
        
        # 检查文件大小
        file_size = os.path.getsize(self.filepath) if os.path.exists(self.filepath) else 0
        is_large_file = file_size >= 10 * 1024  # 10KB
        
        # 根据文件类型选择策略
        for file_type, settings in self.config.get('FILE_TYPES', {}).items():
            if ext in settings.get('extensions', []):
                strategy_name = settings.get('strategy', 'DEFAULT')
                strategy = self.config.get('EDIT_STRATEGIES', {}).get(strategy_name, 
                                                                     self.config['EDIT_STRATEGIES']['DEFAULT'])
                
                # 如果是关键路径或大文件，使用更严格的策略
                if is_critical_path:
                    critical_strategy = self.config.get('EDIT_STRATEGIES', {}).get('CRITICAL_FILE', 
                                                                                 self.config['EDIT_STRATEGIES']['DEFAULT'])
                    strategy.update(critical_strategy)
                elif is_large_file:
                    large_strategy = self.config.get('EDIT_STRATEGIES', {}).get('LARGE_FILE', 
                                                                               self.config['EDIT_STRATEGIES']['DEFAULT'])
                    strategy.update(large_strategy)
                
                return strategy
        
        # 默认策略
        return self.config['EDIT_STRATEGIES'].get('DEFAULT', 
                                                 {'backup': True, 'max_retries': 3, 'delay': 0.1})
    
    def _matches_path_pattern(self, filepath: str, pattern: str) -> bool:
        """检查文件路径是否匹配模式"""
        import fnmatch
        return fnmatch.fnmatch(filepath, pattern) or fnmatch.fnmatch(os.path.basename(filepath), pattern)
        
    def create_backup(self) -> bool:
        """创建备份文件"""
        try:
            timestamp = int(time.time())
            backup_path = f"{self.filepath}.backup.{timestamp}"
            shutil.copy2(self.filepath, backup_path)
            
            # 清理旧备份，只保留最新的几个
            self._cleanup_old_backups()
            
            self.logger.info(f"备份已创建: {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"备份失败: {e}")
            return False
    
    def _should_validate_syntax(self) -> bool:
        """检查是否应该验证语法"""
        _, ext = os.path.splitext(self.filepath)
        ext = ext.lower()
        
        for file_type, settings in self.config.get('FILE_TYPES', {}).items():
            if ext in settings.get('extensions', []) and settings.get('syntax_check', False):
                return True
        return False
    
    def _cleanup_old_backups(self):
        """清理旧备份文件"""
        try:
            dir_path = os.path.dirname(self.filepath)
            filename = os.path.basename(self.filepath)
            backup_pattern = f"{filename}.backup."
            
            backups = []
            for item in os.listdir(dir_path):
                if item.startswith(backup_pattern):
                    full_path = os.path.join(dir_path, item)
                    if os.path.isfile(full_path):
                        backups.append((full_path, os.path.getmtime(full_path)))
            
            # 按修改时间排序，保留最新的
            backups.sort(key=lambda x: x[1], reverse=True)
            
            # 删除多余的备份
            for backup_path, _ in backups[self.backup_count:]:
                os.remove(backup_path)
                self.logger.info(f"删除旧备份: {backup_path}")
                
        except Exception as e:
            self.logger.error(f"清理备份失败: {e}")
    
    def read_with_retry(self, max_retries: int = None, delay: float = None) -> Optional[str]:
        """带重试机制的文件读取"""
        if max_retries is None:
            max_retries = self.strategy.get('max_retries', self.config['GENERAL']['MAX_RETRIES'])
        if delay is None:
            delay = self.strategy.get('delay', self.config['GENERAL']['INITIAL_DELAY'])
            
        for attempt in range(max_retries):
            try:
                with open(self.filepath, 'r', encoding='utf-8', newline='') as f:
                    content = f.read()
                self.logger.info(f"成功读取文件 (尝试 {attempt + 1})")
                return content
            except (IOError, OSError) as e:
                self.logger.warning(f"读取失败 (尝试 {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay * (2 ** attempt))  # 指数退避
                else:
                    self.logger.error("所有读取尝试都失败了")
                    return None
            except UnicodeDecodeError as e:
                self.logger.error(f"编码错误: {e}")
                # 尝试用其他编码读取
                for encoding in ['gbk', 'latin-1', 'cp1252']:
                    try:
                        with open(self.filepath, 'r', encoding=encoding, newline='') as f:
                            content = f.read()
                        self.logger.info(f"使用 {encoding} 编码成功读取")
                        return content
                    except:
                        continue
                return None
        return None
    
    def write_with_retry(self, content: str, max_retries: int = None, delay: float = None) -> bool:
        """带重试机制的安全文件写入"""
        if max_retries is None:
            max_retries = self.strategy.get('max_retries', self.config['GENERAL']['MAX_RETRIES'])
        if delay is None:
            delay = self.strategy.get('delay', self.config['GENERAL']['INITIAL_DELAY'])
        
        # 检查保护规则
        if not self._check_protection_rules(content):
            return False
        
        for attempt in range(max_retries):
            try:
                # 使用临时文件进行原子写入
                temp_dir = os.path.dirname(self.filepath)
                temp_suffix = os.path.splitext(self.filepath)[1] + '.tmp'
                
                with tempfile.NamedTemporaryFile(
                    mode='w', 
                    dir=temp_dir, 
                    delete=False, 
                    suffix=temp_suffix,
                    encoding='utf-8',
                    newline=''
                ) as tmp_file:
                    tmp_file.write(content)
                    tmp_file.flush()
                    os.fsync(tmp_file.fileno())  # 强制同步到磁盘
                    temp_path = tmp_file.name
                
                # 原子替换
                shutil.move(temp_path, self.filepath)
                
                self.logger.info(f"成功写入文件 (尝试 {attempt + 1})")
                return True
                
            except (IOError, OSError) as e:
                # 清理失败的临时文件
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
                
                self.logger.warning(f"写入失败 (尝试 {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay * (2 ** attempt))  # 指数退避
                else:
                    self.logger.error("所有写入尝试都失败了")
                    return False
        return False
    
    def _check_protection_rules(self, new_content: str) -> bool:
        """检查保护规则"""
        rules = self.config.get('PROTECTION_RULES', {})
        
        # 检查空文件写入保护
        if rules.get('PREVENT_EMPTY_WRITE', True) and not new_content.strip():
            self.logger.error("违反保护规则：不允许写入空内容")
            return False
        
        # 检查文件大小变化限制
        if os.path.exists(self.filepath):
            original_size = os.path.getsize(self.filepath)
            new_size = len(new_content.encode('utf-8'))
            
            size_limit = rules.get('SIZE_CHANGE_LIMIT', 3.0)
            if new_size > original_size * size_limit:
                self.logger.error(f"违反保护规则：新内容大小 ({new_size}) 超过原内容大小 ({original_size}) 的 {size_limit} 倍")
                return False
        
        # 检查危险模式
        dangerous_patterns = rules.get('DANGEROUS_PATTERNS', [])
        for pattern in dangerous_patterns:
            if re.search(pattern, new_content):
                self.logger.error(f"违反保护规则：检测到危险模式 '{pattern}'")
                return False
        
        return True
    
    def safe_replace_content(self, old_text: str, new_text: str, backup: bool = True) -> bool:
        """安全的内容替换"""
        # 创建备份
        if backup and not self.create_backup():
            return False
        
        # 读取文件
        content = self.read_with_retry()
        if content is None:
            return False
        
        # 检查是否存在要替换的文本
        if old_text not in content:
            self.logger.warning("要替换的文本不存在")
            return False
        
        # 执行替换
        new_content = content.replace(old_text, new_text)
        
        # 验证替换结果（防止意外的大规模变化）
        if len(new_content) > len(content) * 3:  # 新内容不应超过原内容的3倍
            self.logger.error("替换后内容异常增长，可能存在错误")
            return False
        
        # 写入文件
        return self.write_with_retry(new_content)
    
    def safe_insert_at_line(self, line_number: int, text: str, backup: bool = True) -> bool:
        """在指定行插入文本"""
        if backup and not self.create_backup():
            return False
        
        content = self.read_with_retry()
        if content is None:
            return False
        
        lines = content.splitlines(keepends=True)
        
        if line_number < 0 or line_number > len(lines):
            self.logger.error(f"行号 {line_number} 超出范围 (0-{len(lines)})")
            return False
        
        # 插入文本
        lines.insert(line_number, text + ('\n' if not text.endswith('\n') else ''))
        new_content = ''.join(lines)
        
        return self.write_with_retry(new_content)
    
    def safe_replace_regex(self, pattern: str, replacement: str, backup: bool = True) -> bool:
        """使用正则表达式安全替换"""
        if backup and not self.create_backup():
            return False
        
        content = self.read_with_retry()
        if content is None:
            return False
        
        # 使用正则替换
        new_content, count = re.subn(pattern, replacement, content)
        
        if count == 0:
            self.logger.warning(f"正则表达式 '{pattern}' 未匹配到任何内容")
            return False
        
        self.logger.info(f"正则替换成功，匹配 {count} 处")
        
        return self.write_with_retry(new_content)
    
    def safe_append_content(self, text: str, backup: bool = True) -> bool:
        """安全追加内容到文件末尾"""
        if backup and not self.create_backup():
            return False
        
        content = self.read_with_retry()
        if content is None:
            return False
        
        new_content = content + text
        
        return self.write_with_retry(new_content)
    
    def validate_file_integrity(self) -> bool:
        """验证文件完整性"""
        try:
            # 检查文件是否存在
            if not os.path.exists(self.filepath):
                self.logger.error("文件不存在")
                return False
            
            # 检查文件是否可读
            with open(self.filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否需要语法验证
            if self._should_validate_syntax():
                if self.filepath.endswith('.py'):
                    try:
                        compile(content, self.filepath, 'exec')
                    except SyntaxError as e:
                        self.logger.error(f"Python语法错误: {e}")
                        return False
                elif self.filepath.endswith('.json'):
                    try:
                        json.loads(content)
                    except json.JSONDecodeError as e:
                        self.logger.error(f"JSON格式错误: {e}")
                        return False
                elif self.filepath.endswith(('.yaml', '.yml')):
                    try:
                        yaml.safe_load(content)
                    except yaml.YAMLError as e:
                        self.logger.error(f"YAML格式错误: {e}")
                        return False
            
            return True
        except Exception as e:
            self.logger.error(f"完整性验证失败: {e}")
            return False


def segment_edit_file(filepath: str, operations: List[Tuple[str, dict]], backup: bool = True) -> bool:
    """
    分段编辑文件 - 支持多种操作类型
    
    operations: [
        ('replace', {'old_text': '...', 'new_text': '...'}),
        ('insert_at_line', {'line_number': 10, 'text': '...'}),
        ('regex_replace', {'pattern': '...', 'replacement': '...'}),
        ('append', {'text': '...'})
    ]
    """
    editor = SafeFileEditor(filepath)
    
    # 验证文件完整性
    if not editor.validate_file_integrity():
        return False
    
    for op_type, params in operations:
        if op_type == 'replace':
            success = editor.safe_replace_content(
                params['old_text'], 
                params['new_text'], 
                backup=params.get('backup', backup)
            )
        elif op_type == 'insert_at_line':
            success = editor.safe_insert_at_line(
                params['line_number'], 
                params['text'], 
                backup=params.get('backup', backup)
            )
        elif op_type == 'regex_replace':
            success = editor.safe_replace_regex(
                params['pattern'], 
                params['replacement'], 
                backup=params.get('backup', backup)
            )
        elif op_type == 'append':
            success = editor.safe_append_content(
                params['text'], 
                backup=params.get('backup', backup)
            )
        else:
            logging.error(f"未知的操作类型: {op_type}")
            continue
        
        if not success:
            logging.error(f"操作失败: {op_type}")
            return False
    
    # 最终验证
    return editor.validate_file_integrity()


# 使用示例
if __name__ == "__main__":
    # 示例：安全编辑 channels.py 文件
    filepath = "/home/admin/.openclaw/workspace/ting/backend/app/models/channels.py"
    
    # 定义要执行的操作序列
    operations = [
        # ('replace', {
        #     'old_text': 'qr_code_url = Column(Text)  # 二维码链接',
        #     'new_text': 'qr_code_url = Column(Text)  # 二维码链接\n    logo_url = Column(Text)  # Logo链接'
        # }),
        # ('append', {
        #     'text': '\n# 新增的注释或代码\n'
        # })
    ]
    
    if segment_edit_file(filepath, operations):
        print("文件编辑成功")
    else:
        print("文件编辑失败")