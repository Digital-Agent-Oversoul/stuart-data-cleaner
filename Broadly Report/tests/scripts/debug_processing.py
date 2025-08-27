import pandas as pd
import sys
import os
from alert_contact_export_with_llm import llm_parse_name, extract_name_from_field, extract_name_from_email, is_company_name

def debug_name_extraction():
    print("🔍 Debugging name extraction process...")
    
    # Read the input file
    input_file = "Broadly RAW/Broadly - 7.29.25-8.04.25 - RawData.xlsx"
    df = pd.read_excel(input_file, sheet_name='slsp', header=2)
    
    print(f"📊 Input shape: {df.shape}")
    
    # Test first 5 rows
    for idx in range(5):
        row = df.iloc[idx]
        
        print(f"\n--- Row {idx + 1} ---")
        print(f"Email: {row.get('Email', 'N/A')}")
        print(f"Contact Name: {row.get('Contact Name', 'N/A')}")
        print(f"Customer Name: {row.get('Customer Name', 'N/A')}")
        
        # Test LLM parsing
        contact_name = str(row.get('Contact Name', '')) if not pd.isna(row.get('Contact Name')) else ""
        customer_name = str(row.get('Customer Name', '')) if not pd.isna(row.get('Customer Name')) else ""
        email = str(row.get('Email', '')) if not pd.isna(row.get('Email')) else ""
        
        print(f"LLM Input - Contact: '{contact_name}', Customer: '{customer_name}', Email: '{email}'")
        
        try:
            first_name, last_name = llm_parse_name(contact_name, customer_name, email)
            print(f"LLM Result: First='{first_name}', Last='{last_name}'")
        except Exception as e:
            print(f"LLM Error: {e}")
        
        # Test rule-based parsing
        contact_first, contact_last = extract_name_from_field(row.get('Contact Name'))
        customer_first, customer_last = extract_name_from_field(row.get('Customer Name'))
        email_first, email_last = extract_name_from_email(row.get('Email')) if row.get('Email') and not pd.isna(row.get('Email')) else (None, None)
        
        print(f"Rule-based - Contact: {contact_first}/{contact_last}")
        print(f"Rule-based - Customer: {customer_first}/{customer_last}")
        print(f"Rule-based - Email: {email_first}/{email_last}")
        
        # Test company name detection
        is_customer_company = is_company_name(row.get('Customer Name'))
        print(f"Customer is company: {is_customer_company}")

if __name__ == "__main__":
    debug_name_extraction() 