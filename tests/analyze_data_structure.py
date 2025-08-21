#!/usr/bin/env python3
"""
Data Structure Analysis Script

This script analyzes the raw data structure to understand column mapping.
"""

import pandas as pd
import sys
from pathlib import Path

def analyze_data_structure():
    """Analyze the data structure and column mapping"""
    print("🔍 Analyzing Data Structure")
    print("=" * 50)
    
    # Load the dataset
    data_file = r"C:\LocalAI\!projects\Stuart\Broadly Report\Broadly RAW\Broadly - 7.29.25-8.04.25 - RawData.xlsx"
    df = pd.read_excel(data_file)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Total columns: {len(df.columns)}")
    print()
    
    # Show column mapping
    print("Column Mapping Analysis:")
    print("-" * 30)
    for i, col in enumerate(df.columns):
        print(f"Column {i}: '{col}'")
    print()
    
    # Clean data and show actual content
    df_clean = df.dropna(how='all')
    df_data = df_clean.iloc[1:4]  # Skip header, show first 3 data rows
    
    print("First 3 rows of actual data:")
    print("-" * 30)
    
    for idx, row in df_data.iterrows():
        print(f"\nRow {idx}:")
        for i, col in enumerate(df.columns):
            if pd.notna(row[col]) and str(row[col]).strip():
                print(f"  Column {i} ('{col}'): {row[col]}")
    
    print()
    
    # Identify key columns based on content
    print("Key Column Identification:")
    print("-" * 30)
    
    # Look for columns that might contain contact names, customer names, and emails
    contact_name_col = None
    customer_name_col = None
    email_col = None
    
    for i, col in enumerate(df.columns):
        col_content = str(df_data.iloc[0, i]) if i < len(df_data.columns) else ""
        
        if "MURTY, CIAN" in col_content or "UCB EXTERNAL RELATIONS" in col_content:
            contact_name_col = i
            print(f"Contact Name column: {i} ('{col}')")
        elif "MENDOCINO MUSIC FESTIVAL" in col_content:
            customer_name_col = i
            print(f"Customer Name column: {i} ('{col}')")
        elif "@" in col_content:
            email_col = i
            print(f"Email column: {i} ('{col}')")
    
    print()
    print("Recommended column mapping:")
    print(f"contact_name -> Column {contact_name_col} ('{df.columns[contact_name_col] if contact_name_col is not None else 'NOT FOUND'}')")
    print(f"customer_name -> Column {customer_name_col} ('{df.columns[customer_name_col] if customer_name_col is not None else 'NOT FOUND'}')")
    print(f"email -> Column {email_col} ('{df.columns[email_col] if email_col is not None else 'NOT FOUND'}')")

if __name__ == "__main__":
    analyze_data_structure()
