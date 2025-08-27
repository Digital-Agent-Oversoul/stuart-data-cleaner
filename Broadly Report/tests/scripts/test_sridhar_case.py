import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from alert_contact_export_with_llm import llm_parse_name

def test_sridhar_case():
    print("🧪 Testing SRIDHAR LAKSHMIKANTHAN case...")
    
    contact_name = "SRIDHAR LAKSHMIKANTHAN"
    customer_name = "CHINMAYA MISSION SAN JOSE"
    email = "sridhar@cmsj.org"
    
    print(f"Contact Name: '{contact_name}'")
    print(f"Customer Name: '{customer_name}'")
    print(f"Email: '{email}'")
    print(f"Expected: ('Sridhar', 'Lakshmikanthan')")
    
    result = llm_parse_name(contact_name, customer_name, email)
    
    print(f"Result: {result}")
    
    if result == ('Sridhar', 'Lakshmikanthan'):
        print("✅ PASS")
    else:
        print("❌ FAIL")
        print(f"Expected ('Sridhar', 'Lakshmikanthan'), got {result}")

if __name__ == "__main__":
    test_sridhar_case()
