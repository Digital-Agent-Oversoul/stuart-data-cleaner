import pandas as pd
from alert_contact_export_with_llm import clean_phone

def debug_phone_numbers():
    print("🔍 Debugging phone number processing...")
    
    # Read the input file
    input_file = "Broadly RAW/Broadly - 01.01.25-8.04.25 - RawData.xlsx"
    df = pd.read_excel(input_file, sheet_name='slsp', header=2)
    
    print(f"📊 Input shape: {df.shape}")
    
    # Check phone column
    if 'Phone' in df.columns:
        print(f"📞 Phone column found")
        print(f"   Total rows: {len(df)}")
        print(f"   Non-null phones: {df['Phone'].notna().sum()}")
        print(f"   Null phones: {df['Phone'].isna().sum()}")
        
        # Test first 10 non-null phone numbers
        non_null_phones = df[df['Phone'].notna()].head(10)
        print(f"\n📞 First 10 non-null phone numbers:")
        for idx, row in non_null_phones.iterrows():
            original = row['Phone']
            cleaned = clean_phone(original)
            print(f"   Row {idx}: '{original}' -> '{cleaned}'")
    else:
        print("❌ Phone column not found!")
        print(f"Available columns: {list(df.columns)}")

if __name__ == "__main__":
    debug_phone_numbers() 