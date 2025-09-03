#!/usr/bin/env python3
"""
Manual test/demo of the CLI category functionality.
"""

import tempfile
import os
import subprocess
import sys

def run_dirmarks_command(args):
    """Run dirmarks command and return output."""
    cmd = [sys.executable, '-m', 'dirmarks.main'] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
    return result.stdout, result.stderr, result.returncode

def main():
    print("=== CLI Category Functionality Demo ===\n")
    
    # Create test directories
    test_dirs = []
    for i in range(3):
        test_dirs.append(tempfile.mkdtemp())
    
    print("1. Adding bookmarks with categories:")
    print("-" * 40)
    
    # Test adding with category
    stdout, stderr, code = run_dirmarks_command(['--add', 'project1', test_dirs[0], '--category', 'work'])
    print(f"Adding 'project1' with category 'work': {'✓' if code == 0 else '✗'}")
    if stderr:
        print(f"  Error: {stderr.strip()}")
    
    # Test adding with tags
    stdout, stderr, code = run_dirmarks_command(['--add', 'docs', test_dirs[1], '--tag', 'important,reference'])
    print(f"Adding 'docs' with tags 'important,reference': {'✓' if code == 0 else '✗'}")
    if stderr:
        print(f"  Error: {stderr.strip()}")
    
    # Test adding with both
    stdout, stderr, code = run_dirmarks_command(['--add', 'config', test_dirs[2], '--category', 'work', '--tag', 'server,production'])
    print(f"Adding 'config' with category and tags: {'✓' if code == 0 else '✗'}")
    if stderr:
        print(f"  Error: {stderr.strip()}")
    
    print("\n2. Enhanced listing:")
    print("-" * 40)
    
    # Test enhanced listing
    stdout, stderr, code = run_dirmarks_command(['--list'])
    print("Enhanced list output:")
    if stdout:
        for line in stdout.split('\n'):
            if line.strip():
                print(f"  {line}")
    if stderr:
        print(f"Error: {stderr.strip()}")
    
    print("\n3. Category filtering:")
    print("-" * 40)
    
    # Test category filtering
    stdout, stderr, code = run_dirmarks_command(['--list', '--category', 'work'])
    print("Bookmarks in 'work' category:")
    if stdout:
        for line in stdout.split('\n'):
            if line.strip():
                print(f"  {line}")
    
    print("\n4. Tag filtering:")
    print("-" * 40)
    
    # Test tag filtering
    stdout, stderr, code = run_dirmarks_command(['--list', '--tag', 'important'])
    print("Bookmarks with 'important' tag:")
    if stdout:
        for line in stdout.split('\n'):
            if line.strip():
                print(f"  {line}")
    
    print("\n5. Help with new features:")
    print("-" * 40)
    
    # Test help
    stdout, stderr, code = run_dirmarks_command(['--help'])
    if stderr:  # Help is printed to stderr
        lines = stderr.split('\n')
        # Show only the new category features
        in_category_section = False
        for line in lines:
            if 'Category and tag support' in line:
                in_category_section = True
            if in_category_section:
                print(f"  {line}")
    
    # Clean up
    for d in test_dirs:
        try:
            os.rmdir(d)
        except:
            pass
    
    print("\n=== CLI Demo Complete ===")

if __name__ == "__main__":
    main()