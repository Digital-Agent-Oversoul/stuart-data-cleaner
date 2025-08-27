import pandas as pd
import sys
import os

def debug_data_scrambling(input_file, output_file):
    """Compare raw input with processed output to identify data scrambling"""
    print(f"🔍 Debugging data scrambling...")
    print(f"📁 Input: {input_file}")
    print(f"📁 Output: {output_file}")
    
    # Read raw input data
    print("\n📊 RAW INPUT DATA:")
    df_raw = pd.read_excel(input_file, sheet_name='slsp', header=2)
    print(f"Shape: {df_raw.shape}")
    print(f"Columns: {list(df_raw.columns)}")
    
    # Show first few rows of raw data
    print("\nFirst 5 rows of raw data:")
    raw_display_cols = ['Email', 'Contact Name', 'Customer Name', 'Phone', 'Salesperson']
    available_cols = [col for col in raw_display_cols if col in df_raw.columns]
    print(df_raw[available_cols].head())
    
    # Read processed output
    print(f"\n📊 PROCESSED OUTPUT DATA:")
    df_output = pd.read_excel(output_file)
    print(f"Shape: {df_output.shape}")
    print(f"Columns: {list(df_output.columns)}")
    
    # Show first few rows of output
    print("\nFirst 5 rows of output:")
    output_display_cols = ['Email', 'First name', 'Last name', 'Customer name', 'Phone number', 'Sales person']
    available_cols = [col for col in output_display_cols if col in df_output.columns]
    print(df_output[available_cols].head())
    
    # Check for specific issues
    print(f"\n🔍 SPECIFIC ISSUES:")
    
    # Check phone number formatting
    if 'Phone number' in df_output.columns:
        phone_sample = df_output['Phone number'].head(10)
        print(f"Phone number sample (first 10):")
        for i, phone in enumerate(phone_sample):
            print(f"  {i}: {phone} (type: {type(phone)})")
    
    # Check for duplicate emails
    if 'Email' in df_output.columns:
        email_counts = df_output['Email'].value_counts()
        duplicates = email_counts[email_counts > 1]
        if len(duplicates) > 0:
            print(f"\n⚠️  Found {len(duplicates)} emails with duplicates:")
            print(duplicates.head())
    
    # Check for company names in person name fields
    if 'First name' in df_output.columns and 'Last name' in df_output.columns:
        company_indicators = ['LLC', 'INC', 'CORP', 'GROUP', 'COMPANY', 'RESTAURANT', 'FESTIVAL', 'AMERICAS']
        suspicious_names = []
        for idx, row in df_output.head(20).iterrows():
            first = str(row.get('First name', ''))
            last = str(row.get('Last name', ''))
            for indicator in company_indicators:
                if indicator.upper() in first.upper() or indicator.upper() in last.upper():
                    suspicious_names.append((idx, first, last, indicator))
        
        if suspicious_names:
            print(f"\n⚠️  Found {len(suspicious_names)} suspicious names (possible company names):")
            for idx, first, last, indicator in suspicious_names:
                print(f"  Row {idx}: '{first}' '{last}' (contains '{indicator}')")
    
    # Check for name/email mismatches
    print(f"\n🔍 NAME/EMAIL MATCHING ANALYSIS:")
    print("Comparing raw input with processed output...")
    
    # Create a mapping of raw data
    raw_mapping = {}
    for idx, row in df_raw.iterrows():
        email = str(row.get('Email', '')).strip()
        contact_name = str(row.get('Contact Name', '')).strip()
        customer_name = str(row.get('Customer Name', '')).strip()
        if email and email != 'nan':
            raw_mapping[email] = {
                'contact_name': contact_name,
                'customer_name': customer_name,
                'row_idx': idx
            }
    
    # Check if output matches raw data
    mismatches = []
    for idx, row in df_output.head(10).iterrows():
        output_email = str(row.get('Email', '')).strip()
        output_first = str(row.get('First name', '')).strip()
        output_last = str(row.get('Last name', '')).strip()
        
        if output_email in raw_mapping:
            raw_data = raw_mapping[output_email]
            raw_contact = raw_data['contact_name']
            raw_customer = raw_data['customer_name']
            
            # Check if the names make sense
            if raw_contact and raw_contact != 'nan':
                # Check if output names are reasonable given raw contact name
                if raw_contact.upper() != 'MCKENNA' and 'MCKENNA' in raw_contact.upper():
                    # This might be a mismatch
                    mismatches.append({
                        'email': output_email,
                        'raw_contact': raw_contact,
                        'raw_customer': raw_customer,
                        'output_first': output_first,
                        'output_last': output_last,
                        'issue': 'Possible name mismatch'
                    })
        else:
            mismatches.append({
                'email': output_email,
                'raw_contact': 'NOT FOUND',
                'raw_customer': 'NOT FOUND',
                'output_first': output_first,
                'output_last': output_last,
                'issue': 'Email not found in raw data'
            })
    
    if mismatches:
        print(f"\n⚠️  Found {len(mismatches)} potential mismatches:")
        for mismatch in mismatches:
            print(f"  Email: {mismatch['email']}")
            print(f"    Raw Contact: {mismatch['raw_contact']}")
            print(f"    Raw Customer: {mismatch['raw_customer']}")
            print(f"    Output: {mismatch['output_first']} {mismatch['output_last']}")
            print(f"    Issue: {mismatch['issue']}")
            print()
    else:
        print("✅ No obvious name/email mismatches found in first 10 rows")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python debug_data_scrambling.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)
    
    if not os.path.exists(output_file):
        print(f"❌ Output file not found: {output_file}")
        sys.exit(1)
    
    debug_data_scrambling(input_file, output_file) 