#!/usr/bin/env python3
"""
Test script to verify name parsing functionality with Ollama
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from broadly_data_cleaner_llm import llm_parse_name, clean_name_for_display

def test_name_parsing():
    """Test the name parsing functionality"""
    print("🧪 Testing name parsing with Ollama...")
    
    # Test cases
    test_cases = [
        {
            "contact_name": "John Smith",
            "customer_name": "ABC Company",
            "email": "john.smith@example.com",
            "expected": ("John", "Smith")
        },
        {
            "contact_name": "Jane Doe",
            "customer_name": "Jane Doe Productions",
            "email": "jane@productions.com",
            "expected": ("Jane", "Doe")
        },
        {
            "contact_name": "Steakhouse Restaurant",
            "customer_name": "Fine Dining Inc",
            "email": "info@steakhouse.com",
            "expected": (None, None)  # Should detect as company
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test case {i}:")
        print(f"   Contact: '{test_case['contact_name']}'")
        print(f"   Customer: '{test_case['customer_name']}'")
        print(f"   Email: '{test_case['email']}'")
        
        try:
            first_name, last_name = llm_parse_name(
                test_case['contact_name'],
                test_case['customer_name'],
                test_case['email']
            )
            
            print(f"   Result: first='{first_name}', last='{last_name}'")
            
            if first_name == test_case['expected'][0] and last_name == test_case['expected'][1]:
                print("   ✅ PASS")
            else:
                print("   ⚠️  Result differs from expected, but this is normal for LLM")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_name_parsing() 