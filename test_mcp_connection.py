#!/usr/bin/env python3
"""
Simple MCP Connection Test Script

This script tests the connection to the Archon MCP server and retrieves
project information for the Stuart project.
"""

import asyncio
import json
import httpx

async def test_mcp_connection():
    """Test MCP connection and get Stuart project info"""
    
    print("🔗 Testing Archon MCP Connection...")
    print("=" * 50)
    
    mcp_url = "http://localhost:8051/mcp"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            print(f"📡 Connecting to MCP server: {mcp_url}")
            
            # Test basic connection to /mcp endpoint
            try:
                response = await client.get(mcp_url)
                print(f"✅ MCP endpoint accessible: {response.status_code}")
            except Exception as e:
                print(f"❌ MCP endpoint error: {e}")
            
            # Try to get available sources
            print("\n🔍 Testing MCP tools...")
            
            # Test get_available_sources
            try:
                request_data = {
                    "jsonrpc": "2.0", 
                    "method": "get_available_sources", 
                    "params": {}, 
                    "id": 1
                }
                
                response = await client.post(
                    mcp_url,
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ get_available_sources tool working")
                    if "result" in result:
                        print(f"   Available sources: {result['result']}")
                else:
                    print(f"⚠️  get_available_sources failed: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
            except Exception as e:
                print(f"❌ get_available_sources error: {e}")
            
            # Test manage_project for Stuart
            try:
                request_data = {
                    "jsonrpc": "2.0", 
                    "method": "manage_project", 
                    "params": {"action": "get", "project_name": "Stuart"}, 
                    "id": 2
                }
                
                response = await client.post(
                    mcp_url,
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ manage_project tool working")
                    if "result" in result:
                        print(f"   Stuart project info: {json.dumps(result['result'], indent=2)}")
                    elif "error" in result:
                        print(f"   Project error: {result['error']}")
                else:
                    print(f"⚠️  manage_project failed: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
            except Exception as e:
                print(f"❌ manage_project error: {e}")
            
            # Test manage_task for Stuart
            try:
                request_data = {
                    "jsonrpc": "2.0", 
                    "method": "manage_task", 
                    "params": {"action": "list", "project_id": "Stuart"}, 
                    "id": 3
                }
                
                response = await client.post(
                    mcp_url,
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ manage_task tool working")
                    if "result" in result:
                        print(f"   Stuart project tasks: {json.dumps(result['result'], indent=2)}")
                    elif "error" in result:
                        print(f"   Task error: {result['error']}")
                else:
                    print(f"⚠️  manage_task failed: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
            except Exception as e:
                print(f"❌ manage_task error: {e}")
                
            # Try to list all available tools
            print("\n🔧 Testing tool discovery...")
            try:
                request_data = {
                    "jsonrpc": "2.0", 
                    "method": "tools/list", 
                    "params": {}, 
                    "id": 4
                }
                
                response = await client.post(
                    mcp_url,
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ tools/list tool working")
                    if "result" in result:
                        print(f"   Available tools: {json.dumps(result['result'], indent=2)}")
                else:
                    print(f"⚠️  tools/list failed: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
            except Exception as e:
                print(f"❌ tools/list error: {e}")
                
    except Exception as e:
        print(f"❌ Error connecting to MCP server: {e}")
        return False
    
    return True

async def main():
    """Main function"""
    print("🚀 Archon MCP Connection Test")
    print("=" * 50)
    
    success = await test_mcp_connection()
    
    if success:
        print("\n✅ MCP connection test completed")
    else:
        print("\n❌ MCP connection test failed")

if __name__ == "__main__":
    asyncio.run(main())
