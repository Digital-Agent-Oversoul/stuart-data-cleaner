#!/usr/bin/env python3
"""
OpenAI API Key Test Script

This script tests the OpenAI API key directly to diagnose authentication issues.
"""

import json
import sys
from pathlib import Path

def test_api_key():
    """Test the OpenAI API key directly"""
    print("🔑 Testing OpenAI API Key")
    print("=" * 40)
    
    # Load configuration from the correct path
    config_file = Path(__file__).parent.parent / "test_config.json"
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    api_key = config['openai']['api_key']
    model = config['openai']['model']
    
    print(f"API Key: {api_key[:20]}...{api_key[-4:]}")
    print(f"Model: {model}")
    print()
    
    try:
        import openai
        
        # Test with different API key formats
        print("🧪 Testing API key formats...")
        
        # Test 1: Direct assignment
        print("Test 1: Direct assignment")
        openai.api_key = api_key
        
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=5,
            temperature=0
        )
        print(f"✅ Success! Response: {response.choices[0].message.content}")
        print(f"   Usage: {response.usage}")
        
        # Test 2: Environment variable
        print("\nTest 2: Environment variable")
        import os
        os.environ['OPENAI_API_KEY'] = api_key
        
        # Create new client
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=5,
            temperature=0
        )
        print(f"✅ Success! Response: {response.choices[0].message.content}")
        print(f"   Usage: {response.usage}")
        
        # Test 3: Client with api_key parameter
        print("\nTest 3: Client with api_key parameter")
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=5,
            temperature=0
        )
        print(f"✅ Success! Response: {response.choices[0].message.content}")
        print(f"   Usage: {response.usage}")
        
        print("\n🎉 All API key tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Check if it's an authentication error
        if "401" in str(e) or "authentication" in str(e).lower():
            print("\n🔍 This appears to be an authentication error.")
            print("   Possible causes:")
            print("   1. API key is invalid or expired")
            print("   2. API key doesn't have access to gpt-4o-mini")
            print("   3. Account has insufficient credits")
            print("   4. API key format is incorrect")
        
        return False

if __name__ == "__main__":
    test_api_key()
