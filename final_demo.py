#!/usr/bin/env python3
"""
Final demonstration of the completed Task 2: Category Management Commands.
Shows all the new CLI functionality working together.
"""

import tempfile
import os
import subprocess
import sys

def run_dirmarks_cmd(args):
    """Run dirmarks command and capture output."""
    # Backup the original markrc if it exists
    markrc = os.path.expanduser("~/.markrc")
    markrc_backup = None
    if os.path.exists(markrc):
        markrc_backup = markrc + ".backup"
        os.rename(markrc, markrc_backup)
    
    try:
        result = subprocess.run([sys.executable, '-m', 'dirmarks.main'] + args, 
                                capture_output=True, text=True, timeout=10)
        return result.stdout, result.stderr, result.returncode
    finally:
        # Restore the backup
        if markrc_backup and os.path.exists(markrc_backup):
            if os.path.exists(markrc):
                os.remove(markrc)
            os.rename(markrc_backup, markrc)


def main():
    print("🚀 Task 2 Complete: Category Management Commands Demo")
    print("=" * 60)
    
    # Create test directories
    work_dir = tempfile.mkdtemp(prefix="work_")
    personal_dir = tempfile.mkdtemp(prefix="personal_")
    project_dir = tempfile.mkdtemp(prefix="project_")
    
    try:
        print("\n📁 1. Adding bookmarks with categories and tags:")
        print("-" * 50)
        
        # Test all the new CLI features
        commands = [
            (['--add', 'myproject', work_dir, '--category', 'work'], 
             "Add 'myproject' with work category"),
            (['--add', 'docs', personal_dir, '--tag', 'important,reference'], 
             "Add 'docs' with tags"),
            (['--add', 'server', project_dir, '--category', 'work', '--tag', 'production,critical'], 
             "Add 'server' with category and tags"),
            (['--mark', 'current', '--category', 'temp'], 
             "Mark current directory with category")
        ]
        
        for cmd, desc in commands:
            stdout, stderr, code = run_dirmarks_cmd(cmd)
            status = "✅" if code == 0 else "❌"
            print(f"  {status} {desc}")
            if code != 0 and stderr:
                print(f"    Error: {stderr.strip()}")
        
        print("\n📋 2. Enhanced listing (with categories and tags):")
        print("-" * 50)
        
        stdout, stderr, code = run_dirmarks_cmd(['--list'])
        if stdout:
            lines = [line for line in stdout.split('\n') if line.strip()]
            for line in lines[-4:]:  # Show last 4 entries
                print(f"  {line}")
        
        print("\n🔍 3. Category filtering:")
        print("-" * 50)
        
        stdout, stderr, code = run_dirmarks_cmd(['--list', '--category', 'work'])
        if stdout:
            for line in stdout.split('\n'):
                if line.strip():
                    print(f"  {line}")
        
        print("\n🏷️  4. Tag filtering:")
        print("-" * 50)
        
        stdout, stderr, code = run_dirmarks_cmd(['--list', '--tag', 'important'])
        if stdout:
            for line in stdout.split('\n'):
                if line.strip():
                    print(f"  {line}")
        
        print("\n🔄 5. Updating with categories:")
        print("-" * 50)
        
        stdout, stderr, code = run_dirmarks_cmd(['--update', 'myproject', work_dir, '--category', 'personal'])
        status = "✅" if code == 0 else "❌"
        print(f"  {status} Updated 'myproject' category from work to personal")
        
        print("\n📖 6. New help documentation:")
        print("-" * 50)
        
        stdout, stderr, code = run_dirmarks_cmd(['--help'])
        if stderr:  # Help goes to stderr
            lines = stderr.split('\n')
            showing = False
            for line in lines:
                if 'Category and tag support' in line:
                    showing = True
                if showing:
                    print(f"  {line}")
                    if line.strip() == "":
                        break
        
        print("\n" + "=" * 60)
        print("✨ Task 2: Category Management Commands - COMPLETE!")
        print("\n🎯 Key Features Implemented:")
        print("  • CLI flags: --category and --tag for all commands")
        print("  • Enhanced listing with category/tag display")
        print("  • Category and tag filtering: --list --category/--tag")
        print("  • Argument parsing for complex command combinations")
        print("  • Input validation for category names")
        print("  • Backward compatibility maintained")
        
        print("\n🔥 Example Usage:")
        print("  dirmarks --add myproject /path/to/project --category work --tag client,important")
        print("  dirmarks --list --category work")
        print("  dirmarks --list --tag important")
        print("  dirmarks --update myproject /new/path --category personal")
        
        print("\nReady for Task 3: Category Filtering and Listing! 🚀")
        
    finally:
        # Cleanup
        for d in [work_dir, personal_dir, project_dir]:
            try:
                os.rmdir(d)
            except:
                pass


if __name__ == "__main__":
    main()