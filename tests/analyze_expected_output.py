#!/usr/bin/env python3
"""
Expected Output Structure Analysis

This script analyzes the expected output structure from the example file.
"""

import pandas as pd
import sys
from pathlib import Path

def analyze_expected_output():
    """Analyze the expected output structure"""
    print("🔍 Analyzing Expected Output Structure")
    print("=" * 50)
    
    # Load the example file
    example_file = r"C:\LocalAI\!projects\Stuart\Broadly Report\Alert Contact Export\tests\llmtest000 - Broadly - 01.01.25-8.04.25 - Markup - Alert Contact Export.xlsx"
    
    # Get sheet names
    xl_file = pd.ExcelFile(example_file)
    print(f"Sheet names: {xl_file.sheet_names}")
    print()
    
    # Analyze each sheet
    for sheet_name in xl_file.sheet_names:
        print(f"📋 Sheet: {sheet_name}")
        print("-" * 30)
        
        df = pd.read_excel(example_file, sheet_name=sheet_name)
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        if sheet_name == 'Alert Contact Export':
            print("\nExpected Column Order:")
            for i, col in enumerate(df.columns):
                print(f"  {i+1:2d}. {col}")
        
        print()
        
        # Show first few rows for main sheet
        if sheet_name == 'Alert Contact Export':
            print("First 3 rows:")
            print(df.head(3).to_string())
            print()

if __name__ == "__main__":
    analyze_expected_output()
