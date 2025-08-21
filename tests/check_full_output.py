#!/usr/bin/env python3
"""
Check Full Dataset Output File
"""

import pandas as pd
from pathlib import Path

def check_full_output():
    """Check the full dataset output file"""
    output_file = Path("test_output/full_dataset_contact_export_20250821_014645.xlsx")
    
    if not output_file.exists():
        print(f"❌ Output file not found: {output_file}")
        return
    
    print("🔍 Checking Full Dataset Output File")
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
                print(f"   Sample removed rows:")
                for idx, row in df.head(3).iterrows():
                    contact_name = row.get('contact_name', 'N/A')
                    customer_name = row.get('customer_name', 'N/A')
                    email = row.get('email', 'N/A')
                    salesperson = row.get('Salesperson', 'N/A')
                    print(f"     Row {idx}: Contact='{contact_name}', Customer='{customer_name}', Email='{email}', Salesperson='{salesperson}'")
        
        print()

if __name__ == "__main__":
    check_full_output()
