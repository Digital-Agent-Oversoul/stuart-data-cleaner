import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from alert_contact_export_with_llm import is_company_name

def test_company_detection():
    test_cases = [
        "SRIDHAR",
        "LAKSHMIKANTHAN", 
        "SRIDHAR LAKSHMIKANTHAN",
        "CHINMAYA MISSION SAN JOSE"
    ]
    
    print("🧪 Testing company name detection...")
    
    for name in test_cases:
        is_company = is_company_name(name)
        print(f"'{name}': {'Company' if is_company else 'Person'}")
    
    print("\n🔍 Testing individual parts:")
    parts = "SRIDHAR LAKSHMIKANTHAN".split()
    for part in parts:
        is_company = is_company_name(part)
        print(f"'{part}': {'Company' if is_company else 'Person'}")

if __name__ == "__main__":
    test_company_detection()
