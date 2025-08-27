#!/usr/bin/env python3
"""
Check Fixed Output File v2

This script checks the latest output file to see if the Removed sheet now
properly preserves the original source structure.
"""

import pandas as pd
from pathlib import Path

def check_fixed_output_v2():
    """Check the latest fixed output file"""
    output_file = Path("test_output/full_dataset_contact_export_20250821_020056.xlsx")
    
    if not output_file.exists():
        print(f"❌ Output file not found: {output_file}")
        return
    
    print("🔍 Checking Latest Fixed Output File")
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
                print(f"   Original source column structure:")
                for i, col in enumerate(df.columns):
                    print(f"     {i+1:2d}. {col}")
                
                print(f"\n   Sample removed rows (preserving original structure):")
                for idx, row in df.head(3).iterrows():
                    # Show key fields from original structure
                    contract = row.get('Contracts for Feedback Report', 'N/A')
                    salesperson = row.get('Unnamed: 1', 'N/A')
                    contact_name = row.get('Unnamed: 6', 'N/A')
                    customer_name = row.get('Unnamed: 7', 'N/A')
                    email = row.get('Unnamed: 5', 'N/A')
                    print(f"     Row {idx}: Contract='{contract}', Salesperson='{salesperson}', Contact='{contact_name}', Customer='{customer_name}', Email='{email}'")
        
        print()

if __name__ == "__main__":
    check_fixed_output_v2()
