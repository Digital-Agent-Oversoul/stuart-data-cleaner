#!/usr/bin/env python3
"""
Check Sheet Name Change

This script checks if the output sheet name was successfully changed
from "Alert Contact Export" to "Contact Export".
"""

import pandas as pd
from pathlib import Path

def check_sheet_name_change():
    """Check if the sheet name change took effect"""
    output_file = Path("test_output/full_dataset_contact_export_20250821_021046.xlsx")
    
    if not output_file.exists():
        print(f"❌ Output file not found: {output_file}")
        return
    
    print("🔍 Checking Sheet Name Change")
    print("=" * 50)
    
    # Get sheet names
    xl_file = pd.ExcelFile(output_file)
    print(f"Sheet names: {xl_file.sheet_names}")
    print()
    
    # Check if the main sheet is now named "Contact Export"
    if "Contact Export" in xl_file.sheet_names:
        print("✅ SUCCESS: Main sheet is now named 'Contact Export'")
    elif "Alert Contact Export" in xl_file.sheet_names:
        print("❌ FAILED: Main sheet is still named 'Alert Contact Export'")
    else:
        print("⚠️  UNKNOWN: Main sheet name not found")
    
    # Check if "Removed" sheet is still there
    if "Removed" in xl_file.sheet_names:
        print("✅ SUCCESS: 'Removed' sheet is present")
    else:
        print("❌ FAILED: 'Removed' sheet is missing")
    
    print()
    
    # Show details of each sheet
    for sheet_name in xl_file.sheet_names:
        print(f"📋 Sheet: {sheet_name}")
        print("-" * 30)
        
        df = pd.read_excel(output_file, sheet_name=sheet_name)
        print(f"Shape: {df.shape}")
        
        if sheet_name == "Contact Export":
            print(f"✅ Main output sheet with {len(df)} rows")
            print(f"   Sample data:")
            for idx, row in df.head(2).iterrows():
                print(f"     Row {idx}: {row['First name']} {row['Last name']} - {row['Email']}")
        elif sheet_name == "Removed":
            print(f"🗑️  Removed rows sheet with {len(df)} rows")
            if len(df) > 0:
                print(f"   Sample removed row:")
                row = df.iloc[0]
                contract = row.get('Contract', 'N/A')
                salesperson = row.get('Salesperson', 'N/A')
                print(f"     Contract: {contract}, Salesperson: {salesperson}")
        
        print()

if __name__ == "__main__":
    check_sheet_name_change()
