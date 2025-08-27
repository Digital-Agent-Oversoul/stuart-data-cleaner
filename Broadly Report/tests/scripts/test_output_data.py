import pandas as pd
from alert_contact_export_with_llm import clean_data

def test_output_data():
    print("🔍 Testing output data creation...")
    
    # Process a small file
    input_file = "Broadly RAW/Broadly - 7.29.25-8.04.25 - RawData.xlsx"
    df_output = clean_data(input_file)
    
    print(f"📊 Output shape: {df_output.shape}")
    print(f"📋 Output columns: {list(df_output.columns)}")
    
    # Check phone numbers
    if 'Phone number' in df_output.columns:
        phone_count = df_output['Phone number'].notna().sum()
        print(f"📞 Phone numbers in output: {phone_count}/{len(df_output)}")
        
        # Show first 5 rows with phone numbers
        phones = df_output[df_output['Phone number'].notna()].head(5)
        print(f"\n📞 First 5 rows with phone numbers:")
        for idx, row in phones.iterrows():
            print(f"   Row {idx}: Phone='{row['Phone number']}', First='{row['First name']}', Last='{row['Last name']}'")
    
    # Check names
    if 'First name' in df_output.columns:
        first_count = df_output['First name'].notna().sum()
        print(f"👤 First names in output: {first_count}/{len(df_output)}")
    
    if 'Last name' in df_output.columns:
        last_count = df_output['Last name'].notna().sum()
        print(f"👤 Last names in output: {last_count}/{len(df_output)}")

if __name__ == "__main__":
    test_output_data() 