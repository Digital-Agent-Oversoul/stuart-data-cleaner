#!/usr/bin/env python3
"""
Simple Archon MCP Client Test Script

This script tests the connection to the Archon MCP server and explores
the available tools for project management and knowledge base access.
"""

import json
import requests
import sys
from datetime import datetime

def test_mcp_connection():
    """Test basic connection to Archon MCP server"""
    
    print("🔗 Testing Archon MCP Server Connection")
    print("=" * 50)
    
    base_url = "http://localhost:8051"
    
    # Test 1: Basic health check
    print("\n1️⃣ Testing MCP server health...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check successful")
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"⚠️  Health check returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test 2: MCP endpoint
    print("\n2️⃣ Testing MCP endpoint...")
    try:
        response = requests.get(f"{base_url}/mcp", timeout=10)
        print(f"   MCP endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("✅ MCP endpoint accessible")
        else:
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ MCP endpoint test failed: {e}")
    
    return base_url

def test_mcp_tools(base_url):
    """Test the available MCP tools"""
    
    print("\n🔧 Testing Available MCP Tools")
    print("=" * 50)
    
    # Test 3: Session info
    print("\n3️⃣ Testing session info tool...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "mcp_archon_session_info",
            "params": {},
            "id": 1
        }
        response = requests.post(f"{base_url}/mcp", json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Session info tool working")
            print(f"   Result: {json.dumps(result, indent=2)}")
        else:
            print(f"⚠️  Session info tool returned status {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Session info tool failed: {e}")
    
    # Test 4: Available sources
    print("\n4️⃣ Testing available sources tool...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "mcp_archon_get_available_sources",
            "params": {},
            "id": 2
        }
        response = requests.post(f"{base_url}/mcp", json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Available sources tool working")
            print(f"   Result: {json.dumps(result, indent=2)}")
        else:
            print(f"⚠️  Available sources tool returned status {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Available sources tool failed: {e}")
    
    # Test 5: Project management
    print("\n5️⃣ Testing project management tool...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "mcp_archon_manage_project",
            "params": {
                "action": "list"
            },
            "id": 3
        }
        response = requests.post(f"{base_url}/mcp", json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Project management tool working")
            print(f"   Result: {json.dumps(result, indent=2)}")
        else:
            print(f"⚠️  Project management tool returned status {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Project management tool failed: {e}")

def test_stuart_project(base_url):
    """Test specific Stuart project operations"""
    
    print("\n🏗️  Testing Stuart Project Operations")
    print("=" * 50)
    
    # Test 6: Get Stuart project
    print("\n6️⃣ Testing Stuart project retrieval...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "mcp_archon_manage_project",
            "params": {
                "action": "get",
                "project_name": "Stuart"
            },
            "id": 4
        }
        response = requests.post(f"{base_url}/mcp", json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Stuart project retrieval successful")
            print(f"   Result: {json.dumps(result, indent=2)}")
        else:
            print(f"⚠️  Stuart project retrieval returned status {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Stuart project retrieval failed: {e}")
    
    # Test 7: Get project features
    print("\n7️⃣ Testing project features tool...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "mcp_archon_get_project_features",
            "params": {},
            "id": 5
        }
        response = requests.post(f"{base_url}/mcp", json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Project features tool working")
            print(f"   Result: {json.dumps(result, indent=2)}")
        else:
            print(f"⚠️  Project features tool returned status {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Project features tool failed: {e}")

def main():
    """Main function to run all tests"""
    
    print("🚀 Archon MCP Server Test Suite")
    print(f"   Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Test basic connection
        base_url = test_mcp_connection()
        
        # Test MCP tools
        test_mcp_tools(base_url)
        
        # Test Stuart project specifically
        test_stuart_project(base_url)
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
