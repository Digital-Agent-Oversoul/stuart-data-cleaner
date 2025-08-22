#!/usr/bin/env python3
"""
Import Diagnostic Script

This script helps diagnose and fix import issues in the Stuart Data Cleaner project.
Run this script to check if all required packages are properly installed and accessible.
"""

import sys
import subprocess
from pathlib import Path

def check_package(package_name, import_name=None):
    """Check if a package is installed and can be imported"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name} - FAILED: {e}")
        return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ Installed {package_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("🔍 Stuart Data Cleaner - Import Diagnostic")
    print("=" * 50)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Python path: {sys.path[:3]}...")
    print()
    
    # Required packages
    required_packages = [
        ("pandas", "pandas"),
        ("openpyxl", "openpyxl"),
        ("xlrd", "xlrd"),
        ("openai", "openai"),
        ("requests", "requests"),
        ("numpy", "numpy"),
        ("xlsxwriter", "xlsxwriter")
    ]
    
    print("📦 Checking required packages:")
    failed_packages = []
    
    for package_name, import_name in required_packages:
        if not check_package(package_name, import_name):
            failed_packages.append(package_name)
    
    print()
    
    # Install failed packages if any
    if failed_packages:
        print(f"⚠️  {len(failed_packages)} packages failed to import:")
        for package in failed_packages:
            print(f"   - {package}")
        
        print("\n🔧 Attempting to install failed packages...")
        for package in failed_packages:
            install_package(package)
        
        print("\n🔄 Re-checking packages after installation...")
        for package_name, import_name in required_packages:
            check_package(package_name, import_name)
    else:
        print("🎉 All required packages are properly installed!")
    
    print()
    
    # Test project imports
    print("🧪 Testing project imports:")
    try:
        # Add current directory to Python path
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        # Test core imports
        from core.data_processor import DataProcessor
        print("✅ core.data_processor - OK")
        
        from core.llm_engine import LLMEngine
        print("✅ core.llm_engine - OK")
        
        from core.name_parser import NameParser
        print("✅ core.name_parser - OK")
        
        # Test workflow imports
        from workflows.contact_export.export_processor import ExportProcessor
        print("✅ workflows.contact_export.export_processor - OK")
        
        print("\n🎉 All project imports successful!")
        
    except ImportError as e:
        print(f"❌ Project import failed: {e}")
        print("\n💡 This might be a Python path issue. Try:")
        print("   1. Set PYTHONPATH environment variable")
        print("   2. Use absolute imports")
        print("   3. Check your IDE's Python interpreter configuration")
    
    print("\n" + "=" * 50)
    print("Diagnostic complete!")

if __name__ == "__main__":
    main()
