import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from alert_contact_export_with_llm import is_company_name, extract_name_from_field

def test_hemispherics_case():
    print("🧪 Testing HEMISPHERICS TECH case...")
    
    test_cases = [
        "HEMISPHERICS TECH.",
        "WESTERN HEMISPHERICS TECH.",
        "TECH.",
        "HEMISPHERICS"
    ]
    
    print("Company name detection:")
    for name in test_cases:
        is_company = is_company_name(name)
        print(f"'{name}': {'Company' if is_company else 'Person'}")
    
    print("\nName extraction test:")
    contact_name = "SHEILA"
    customer_name = "DEGREE, INC. DBA  LATTICE"
    email = "SHEILA.SALENGA@LATTICE.COM"
    
    print(f"Contact Name: '{contact_name}'")
    print(f"Customer Name: '{customer_name}'")
    print(f"Email: '{email}'")
    
    # Test extraction from each field
    contact_first, contact_last = extract_name_from_field(contact_name)
    customer_first, customer_last = extract_name_from_field(customer_name)
    
    print(f"Contact extraction: first='{contact_first}', last='{contact_last}'")
    print(f"Customer extraction: first='{customer_first}', last='{customer_last}'")

if __name__ == "__main__":
    test_hemispherics_case()
