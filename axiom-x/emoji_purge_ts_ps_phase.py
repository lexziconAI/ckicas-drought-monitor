#!/usr/bin/env python3
"""
EMOJI PURGE REDTEAM - TypeScript & PowerShell Phase
Removes emoji from *.ts, *.tsx, and *.ps1 files
"""

import os
import re
from pathlib import Path
from typing import Tuple

class EmojiPurgeTS_PS:
    """Emoji removal for TypeScript/TSX and PowerShell files"""
    
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.stats = {
            'ts_files': 0,
            'ps_files': 0,
            'emojis_removed': 0,
            'files_modified': []
        }
        
        # Comprehensive emoji regex patterns
        self.emoji_patterns = [
            r'[\U0001F300-\U0001F9FF]',
            r'[\u2600-\u27BF]', r'[\u2300-\u23FF]', r'[\u2B50-\u2B55]',
            r'[\u1F600-\u1F64F]', r'[\u1F300-\u1F5FF]', r'[\u1F680-\u1F6FF]',
            r'[\u1F1E0-\u1F1FF]', r'[\u2500-\u27FF]', r'[\u1F700-\u1F77F]',
            r'[\u1F780-\u1F7FF]', r'[\u1F800-\u1F8FF]', r'[\u1F900-\u1F9FF]',
            r'[\u1FA00-\u1FA6F]', r'[\u1FA70-\u1FAFF]', r'[\u2000-\u206F]',
            r'[\uFE00-\uFE0F]', r'[\u200D]', r'[\u200B]', r'[\u200C]',
            r'[\u202A-\u202E]', r'[\u061C]',
            r'[✅❌🚀📊📈📉🔄⚠️⚡🎉🔍📱💻🌍🗺️📍📡🔵🟢🟡🟠🔴⭕🟣🟪✓✗]',
        ]
        self.combined_pattern = re.compile('|'.join(self.emoji_patterns))
    
    def sanitize_file(self, filepath: str) -> Tuple[bool, int]:
        """Remove emojis from file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            print(f"[WARN] Cannot read {filepath}: {e}")
            return False, 0
        
        # Count and remove emoji
        count = 0
        def replace_emoji(match):
            nonlocal count
            count += 1
            return ''
        
        new_content = self.combined_pattern.sub(replace_emoji, content)
        
        if count > 0:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True, count
            except Exception as e:
                print(f"[FAIL] Cannot write {filepath}: {e}")
                return False, count
        
        return False, 0
    
    def process_files(self):
        """Process TypeScript and PowerShell files"""
        print(f"\n[LAUNCH] EMOJI PURGE REDTEAM - TypeScript & PowerShell Phase")
        print(f"[INFO] Target: {self.root_dir}")
        
        target_path = Path(self.root_dir)
        skip_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.quarantine'}
        
        # Process TypeScript files
        for ext in ['.ts', '.tsx']:
            ts_files = list(target_path.glob(f"**/*{ext}"))
            print(f"[INFO] Found {len(ts_files)} {ext} files")
            
            for ts_file in ts_files:
                if any(skip_dir in ts_file.parts for skip_dir in skip_dirs):
                    continue
                
                was_modified, count = self.sanitize_file(str(ts_file))
                if was_modified:
                    print(f"[OK] {ts_file.name}: Removed {count} emoji(s)")
                    self.stats['ts_files'] += 1
                    self.stats['emojis_removed'] += count
                    self.stats['files_modified'].append((ts_file.name, count))
        
        # Process PowerShell files
        for ps_file in target_path.glob("**/*.ps1"):
            if any(skip_dir in ps_file.parts for skip_dir in skip_dirs):
                continue
            
            was_modified, count = self.sanitize_file(str(ps_file))
            if was_modified:
                print(f"[OK] {ps_file.name}: Removed {count} emoji(s)")
                self.stats['ps_files'] += 1
                self.stats['emojis_removed'] += count
                self.stats['files_modified'].append((ps_file.name, count))
        
        self.print_report()
    
    def print_report(self):
        """Print summary report"""
        print(f"\n{'='*70}")
        print(f"EMOJI PURGE REDTEAM - TypeScript & PowerShell REPORT")
        print(f"{'='*70}")
        print(f"[OK] TypeScript files processed: {self.stats['ts_files']}")
        print(f"[OK] PowerShell files processed:  {self.stats['ps_files']}")
        print(f"[OK] Total emojis removed:       {self.stats['emojis_removed']}")
        
        if self.stats['files_modified']:
            print(f"\n[INFO] Modified files:")
            for filename, count in sorted(self.stats['files_modified'], key=lambda x: x[1], reverse=True):
                print(f"       {filename}: {count} emoji(s)")
        
        print(f"{'='*70}\n")


if __name__ == "__main__":
    root = r"c:\Users\regan\ID SYSTEM\axiom-x"
    redteam = EmojiPurgeTS_PS(root)
    redteam.process_files()
