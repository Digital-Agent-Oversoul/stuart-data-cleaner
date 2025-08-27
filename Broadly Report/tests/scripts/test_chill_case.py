import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from alert_contact_export_with_llm import is_company_name, extract_name_from_field

def test_chill_case():
    print("🧪 Testing PICNIC AND CHILL case...")
    
    test_cases = [
        "PICNIC AND CHILL",
        "AND CHILL",
        "CHILL",
        "PICNIC"
    ]
    
    print("Company name detection:")
    for name in test_cases:
        is_company = is_company_name(name)
        print(f"'{name}': {'Company' if is_company else 'Person'}")
    
    print("\nName extraction test:")
    contact_name = "JOCELYN"
    customer_name = "PICNIC AND CHILL"
    email = "PICNICANDCHILL@GMAIL.COM"
    
    print(f"Contact Name: '{contact_name}'")
    print(f"Customer Name: '{customer_name}'")
    print(f"Email: '{email}'")
    
    # Test extraction from each field
    contact_first, contact_last = extract_name_from_field(contact_name)
    customer_first, customer_last = extract_name_from_field(customer_name)
    
    print(f"Contact extraction: first='{contact_first}', last='{contact_last}'")
    print(f"Customer extraction: first='{customer_first}', last='{customer_last}'")

if __name__ == "__main__":
    test_chill_case()
