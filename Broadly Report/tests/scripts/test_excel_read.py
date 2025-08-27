import pandas as pd
import os

def test_excel_read():
    print("🔍 Testing Excel file reading...")
    
    output_dir = r"C:\LocalAI\Stuart\broadly\Broadly Report\Alert Contact Export"
    files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx')]
    
    for file in files:
        filepath = os.path.join(output_dir, file)
        print(f"\n📄 Reading: {file}")
        
        try:
            df = pd.read_excel(filepath)
            print(f"   Shape: {df.shape}")
            
            if 'Phone number' in df.columns:
                phone_count = df['Phone number'].notna().sum()
                print(f"   Phone numbers: {phone_count}/{len(df)}")
                
                # Show first 3 phone numbers
                phones = df[df['Phone number'].notna()].head(3)
                for idx, row in phones.iterrows():
                    phone = row['Phone number']
                    print(f"   Row {idx}: Phone='{phone}' (type: {type(phone)})")
            
            if 'First name' in df.columns:
                first_count = df['First name'].notna().sum()
                print(f"   First names: {first_count}/{len(df)}")
            
            if 'Last name' in df.columns:
                last_count = df['Last name'].notna().sum()
                print(f"   Last names: {last_count}/{len(df)}")
                
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")

if __name__ == "__main__":
    test_excel_read() 