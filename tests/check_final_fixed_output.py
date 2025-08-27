#!/usr/bin/env python3
"""
Check Final Fixed Output File

This script checks the final output file to see if the Removed sheet now
shows the proper column headers from row 3 of the source file.
"""

import pandas as pd
from pathlib import Path

def check_final_fixed_output():
    """Check the final fixed output file"""
    output_file = Path("test_output/full_dataset_contact_export_20250821_020629.xlsx")
    
    if not output_file.exists():
        print(f"❌ Output file not found: {output_file}")
        return
    
    print("🔍 Checking Final Fixed Output File")
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
            print(f"\n✅ Main output: {len(df)} rows processed successfully")
            print(f"   Sample data:")
            for idx, row in df.head(3).iterrows():
                print(f"     Row {idx}: {row['First name']} {row['Last name']} - {row['Email']}")
        
        elif sheet_name == 'Removed':
            print(f"\n🗑️  Removed rows: {len(df)} rows removed during processing")
            if len(df) > 0:
                print(f"   Original source column structure (from row 3):")
                for i, col in enumerate(df.columns):
                    print(f"     {i+1:2d}. {col}")
                
                print(f"\n   Sample removed rows (with proper column headers):")
                for idx, row in df.head(3).iterrows():
                    # Show key fields from original structure
                    contract = row.get('Contract', 'N/A')
                    salesperson = row.get('Salesperson', 'N/A')
                    contact_name = row.get('Contact Name', 'N/A')
                    customer_name = row.get('Customer Name', 'N/A')
                    email = row.get('Email', 'N/A')
                    print(f"     Row {idx}: Contract='{contract}', Salesperson='{salesperson}', Contact='{contact_name}', Customer='{customer_name}', Email='{email}'")
        
        print()

if __name__ == "__main__":
    check_final_fixed_output()
