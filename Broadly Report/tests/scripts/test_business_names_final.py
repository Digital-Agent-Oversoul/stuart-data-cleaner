import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from alert_contact_export_with_llm import llm_parse_name

def test_business_names():
    test_cases = [
        {
            'contact_name': '',
            'customer_name': 'SRI ANANDA BHAVAN RESTAURANT',
            'email': 'SABSV1111@GMAIL.COM',
            'expected': (None, None),
            'description': 'Business email with business customer name'
        },
        {
            'contact_name': 'MANTRA',
            'customer_name': 'MANTRA INDIA',
            'email': 'mantraindiacatering@gmail.com',
            'expected': (None, None),
            'description': 'Business contact name with business customer name'
        },
        {
            'contact_name': 'STACY ROCK',
            'customer_name': 'CATERED TOO INC',
            'email': 'AP@CATEREDTOO.COM',
            'expected': ('Stacy', 'Rock'),
            'description': 'Valid person name with business email'
        }
    ]
    
    print("🧪 Testing business name detection...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['description']} ---")
        print(f"Contact Name: '{test_case['contact_name']}'")
        print(f"Customer Name: '{test_case['customer_name']}'")
        print(f"Email: '{test_case['email']}'")
        print(f"Expected: {test_case['expected']}")
        
        result = llm_parse_name(
            test_case['contact_name'],
            test_case['customer_name'],
            test_case['email']
        )
        
        print(f"Result: {result}")
        
        if result == test_case['expected']:
            print("✅ PASS")
        else:
            print("❌ FAIL")
            print(f"Expected {test_case['expected']}, got {result}")

if __name__ == "__main__":
    test_business_names()
