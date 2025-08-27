#!/usr/bin/env python3
"""
Git Commit Script for Stuart Data Cleaner

This script handles git operations to commit all recent changes
including import fixes, documentation updates, and new files.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_git_command(command):
    """Run a git command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.returncode == 0:
            print(f"✅ {command}")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {command}")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {command} - Exception: {e}")
        return False

def main():
    """Main function to commit all changes"""
    print("🚀 Stuart Data Cleaner - Git Commit Script")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not run_git_command("git status"):
        print("❌ Not in a git repository or git not available")
        return
    
    print("\n📋 Current Git Status:")
    run_git_command("git status --porcelain")
    
    print("\n🔧 Adding all files to git...")
    if not run_git_command("git add ."):
        print("❌ Failed to add files")
        return
    
    print("\n📝 Committing changes...")
    commit_message = """Import Error Resolution & Environment Setup

- Resolved pandas import error (Python version mismatch)
- Installed all dependencies for Python 3.12
- Configured virtual environment usage
- Created import diagnostic script (fix_imports.py)
- Updated documentation with setup instructions
- Added comprehensive troubleshooting guides
- Updated project status and changelog

All imports now working correctly. Project ready for continued development."""
    
    if not run_git_command(f'git commit -m "{commit_message}"'):
        print("❌ Failed to commit changes")
        return
    
    print("\n📊 Final Status:")
    run_git_command("git status")
    
    print("\n🎉 All changes committed successfully!")
    print("\n📋 Summary of changes:")
    print("   ✅ Import errors resolved")
    print("   ✅ Environment configured")
    print("   ✅ Documentation updated")
    print("   ✅ New files added")
    print("   ✅ Project status updated")
    
    print("\n🚀 Next steps:")
    print("   1. Continue with Task 3 (Core Data Processing)")
    print("   2. Test with sample datasets")
    print("   3. Complete workflow implementations")

if __name__ == "__main__":
    main()
