import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from alert_contact_export_with_llm import extract_name_from_field

def test_rule_based():
    print("🧪 Testing rule-based name extraction...")
    
    contact_name = "SRIDHAR LAKSHMIKANTHAN"
    customer_name = "CHINMAYA MISSION SAN JOSE"
    email = "sridhar@cmsj.org"
    
    print(f"Contact Name: '{contact_name}'")
    print(f"Customer Name: '{customer_name}'")
    print(f"Email: '{email}'")
    
    # Test the rule-based extraction
    contact_first, contact_last = extract_name_from_field(contact_name)
    customer_first, customer_last = extract_name_from_field(customer_name)
    
    print(f"Contact extraction: first='{contact_first}', last='{contact_last}'")
    print(f"Customer extraction: first='{customer_first}', last='{customer_last}'")
    
    # Build the best possible name
    best_first = None
    best_last = None
    
    # Priority for first name: Contact > Customer
    if contact_first:
        best_first = contact_first
    elif customer_first:
        best_first = customer_first
    
    # Priority for last name: Contact > Customer
    if contact_last:
        best_last = contact_last
    elif customer_last:
        best_last = customer_last
    
    print(f"Best name: first='{best_first}', last='{best_last}'")

if __name__ == "__main__":
    test_rule_based()
