#!/usr/bin/env python3
"""
Check Output File Structure
"""

import pandas as pd
from pathlib import Path

def check_output():
    """Check the output file structure"""
    output_file = Path("test_output/corrected_contact_export_20250821_012745.xlsx")
    
    if not output_file.exists():
        print(f"❌ Output file not found: {output_file}")
        return
    
    print("🔍 Checking Output File Structure")
    print("=" * 40)
    
    # Get sheet names
    xl_file = pd.ExcelFile(output_file)
    print(f"Sheet names: {xl_file.sheet_names}")
    print()
    
    # Analyze each sheet
    for sheet_name in xl_file.sheet_names:
        print(f"📋 Sheet: {sheet_name}")
        print("-" * 30)
        
        df = pd.read_excel(output_file, sheet_name=sheet_name)
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        if sheet_name == 'Alert Contact Export':
            print("\nColumn Order:")
            for i, col in enumerate(df.columns):
                print(f"  {i+1:2d}. {col}")
            
            print("\nFirst 3 rows:")
            print(df.head(3).to_string())
        
        print()

if __name__ == "__main__":
    check_output()
