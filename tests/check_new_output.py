#!/usr/bin/env python3
"""
Check New Corrected Output File
"""

import pandas as pd
from pathlib import Path

def check_new_output():
    """Check the new corrected output file"""
    output_file = Path("test_output/corrected_contact_export_20250821_014009.xlsx")
    
    if not output_file.exists():
        print(f"❌ Output file not found: {output_file}")
        return
    
    print("🔍 Checking New Corrected Output File")
    print("=" * 50)
    
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
            
            print("\nFirst 5 rows with key formatting:")
            print("=" * 60)
            for idx, row in df.head(5).iterrows():
                print(f"Row {idx}:")
                print(f"  Email: '{row['Email']}'")
                print(f"  First name: '{row['First name']}'")
                print(f"  Last name: '{row['Last name']}'")
                print(f"  Phone: '{row['Phone number']}'")
                print(f"  State: '{row['State']}'")
                print()
        
        print()

if __name__ == "__main__":
    check_new_output()
