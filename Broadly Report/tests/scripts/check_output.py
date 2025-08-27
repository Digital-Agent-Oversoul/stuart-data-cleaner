import pandas as pd
import os
import sys

def check_specific_file(filepath):
    """Check a specific output file"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return
    
    print(f"📄 Checking: {filepath}")
    
    try:
        # Read phone numbers as text to prevent conversion to float
        df = pd.read_excel(filepath, dtype={'Phone number': str})
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        
        # Check for missing data
        if 'First name' in df.columns:
            first_name_count = df['First name'].notna().sum()
            print(f"   First name entries: {first_name_count}/{len(df)}")
            if first_name_count == 0:
                print("   ⚠️  NO FIRST NAMES FOUND!")
            else:
                print(f"   Sample first names: {df['First name'].dropna().head(3).tolist()}")
        
        if 'Last name' in df.columns:
            last_name_count = df['Last name'].notna().sum()
            print(f"   Last name entries: {last_name_count}/{len(df)}")
            if last_name_count == 0:
                print("   ⚠️  NO LAST NAMES FOUND!")
            else:
                print(f"   Sample last names: {df['Last name'].dropna().head(3).tolist()}")
        
        if 'Phone number' in df.columns:
            phone_count = df['Phone number'].notna().sum()
            print(f"   Phone number entries: {phone_count}/{len(df)}")
            if phone_count == 0:
                print("   ⚠️  NO PHONE NUMBERS FOUND!")
            else:
                print(f"   Sample phone numbers: {df['Phone number'].dropna().head(3).tolist()}")
        
        # Show first few rows
        print(f"   First 3 rows:")
        print(df.head(3).to_string())
        
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")

def check_output_files():
    output_dir = r"C:\LocalAI\Stuart\broadly\Broadly Report\Alert Contact Export"
    
    if not os.path.exists(output_dir):
        print("❌ Output directory not found")
        return
    
    files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx')]
    print(f"📁 Found {len(files)} output files:")
    
    for file in files:
        filepath = os.path.join(output_dir, file)
        check_specific_file(filepath)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Check specific file
        check_specific_file(sys.argv[1])
    else:
        # Check all files in output directory
        check_output_files() 