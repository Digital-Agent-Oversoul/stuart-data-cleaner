import pandas as pd
import sys
import os

# Add the current directory to the path so we can import from the main script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from alert_contact_export_with_llm import llm_parse_name

def test_business_names():
    """Test the LLM with business name cases that should return None, None"""
    
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
        }
    ]
    
    print("Testing business name detection...")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Contact: '{test_case['contact_name']}'")
        print(f"Customer: '{test_case['customer_name']}'")
        print(f"Email: '{test_case['email']}'")
        
        result = llm_parse_name(
            test_case['contact_name'],
            test_case['customer_name'],
            test_case['email']
        )
        
        print(f"Result: {result}")
        print(f"Expected: {test_case['expected']}")
        
        if result == test_case['expected']:
            print("✅ PASS")
        else:
            print("❌ FAIL")

if __name__ == "__main__":
    test_business_names()
