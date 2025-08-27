import requests
import json
import sys

print("🔍 Debugging LLM connection...")
sys.stdout.flush()

# Test 1: Basic Ollama connection
print("1. Testing Ollama connection...")
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Ollama connection successful")
    else:
        print("   ❌ Ollama connection failed")
except Exception as e:
    print(f"   ❌ Ollama connection error: {e}")

sys.stdout.flush()

# Test 2: Simple LLM call
print("\n2. Testing simple LLM call...")
try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b-instruct-q4_K_M",
            "prompt": "Say 'Hello World'",
            "stream": False,
            "context": [],
            "options": {
                "temperature": 0.1,
                "num_predict": 50
            }
        },
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ LLM response: {result.get('response', '')[:100]}...")
    else:
        print(f"   ❌ LLM call failed: {response.text}")
except Exception as e:
    print(f"   ❌ LLM call error: {e}")

sys.stdout.flush()
print("\n✅ Debug complete!") 