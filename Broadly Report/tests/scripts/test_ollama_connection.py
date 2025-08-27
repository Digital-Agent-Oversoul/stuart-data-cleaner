#!/usr/bin/env python3
"""
Test script to verify Ollama connection and model availability
"""

import requests
import json

def test_ollama_connection():
    """Test connection to Ollama and verify model availability"""
    base_url = "http://localhost:11434"
    
    print("🔍 Testing Ollama connection...")
    
    try:
        # Test basic connection
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama connection successful")
            
            # Get available models
            models = response.json().get('models', [])
            print(f"📋 Available models: {len(models)}")
            
            for model in models:
                print(f"   - {model.get('name', 'Unknown')}")
            
            # Test specific model
            target_model = "phi3:mini"
            model_found = any(model.get('name') == target_model for model in models)
            
            if model_found:
                print(f"✅ Target model '{target_model}' is available")
                
                # Test a simple generation
                print("🧪 Testing model generation...")
                test_response = requests.post(
                    f"{base_url}/api/generate",
                    json={
                        "model": target_model,
                        "prompt": "Return only the JSON: {\"test\": \"success\"}",
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "num_predict": 50
                        }
                    },
                    timeout=30
                )
                
                if test_response.status_code == 200:
                    result = test_response.json()
                    content = result.get('response', '').strip()
                    print(f"✅ Model generation successful")
                    print(f"📝 Response: {content}")
                else:
                    print(f"❌ Model generation failed: {test_response.status_code}")
                    
            else:
                print(f"❌ Target model '{target_model}' not found")
                print("   Available models:")
                for model in models:
                    print(f"     - {model.get('name', 'Unknown')}")
                    
        else:
            print(f"❌ Ollama connection failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        print("   Make sure Ollama is running on localhost:11434")

if __name__ == "__main__":
    test_ollama_connection() 