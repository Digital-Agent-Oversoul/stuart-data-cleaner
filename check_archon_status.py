#!/usr/bin/env python3
"""
Archon MCP Connection Test Script

This script tests the connection to the Archon MCP server and retrieves
project information for the Stuart project.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the Archon Python path to sys.path
archon_path = Path("C:/LocalAI/archon/python/src")
if archon_path.exists():
    sys.path.insert(0, str(archon_path))

try:
    from agents.mcp_client import MCPClient
except ImportError:
    print("Error: Could not import MCPClient from Archon")
    print("Please ensure the Archon Python source is available at C:/LocalAI/archon/python/src")
    sys.exit(1)

async def check_archon_status():
    """Check Archon MCP server status and Stuart project information"""
    
    print("🔗 Connecting to Archon MCP Server...")
    print("=" * 50)
    
    try:
        # Initialize MCP client
        mcp_client = MCPClient("http://localhost:8051")
        
        print("✅ MCP Client initialized successfully")
        print(f"   Server URL: http://localhost:8051")
        
        # Test basic connection
        print("\n📡 Testing MCP connection...")
        
        # Try to get available sources
        try:
            sources = await mcp_client.get_available_sources()
            print("✅ Successfully retrieved available sources")
            print(f"   Sources: {sources}")
        except Exception as e:
            print(f"⚠️  Could not retrieve sources: {e}")
        
        # Try to get session info
        try:
            session_info = await mcp_client.call_tool("mcp_archon_session_info")
            print("✅ Successfully retrieved session info")
            print(f"   Session: {json.dumps(session_info, indent=2)}")
        except Exception as e:
            print(f"⚠️  Could not retrieve session info: {e}")
        
        # Try to manage project (get Stuart project info)
        print("\n🏗️  Checking Stuart project status...")
        try:
            project_info = await mcp_client.manage_project(
                action="get", 
                project_name="Stuart"
            )
            print("✅ Successfully retrieved Stuart project info")
            print(f"   Project: {json.dumps(project_info, indent=2)}")
        except Exception as e:
            print(f"⚠️  Could not retrieve Stuart project: {e}")
        
        # Try to get project features
        try:
            features = await mcp_client.call_tool("mcp_archon_get_project_features")
            print("✅ Successfully retrieved project features")
            print(f"   Features: {json.dumps(features, indent=2)}")
        except Exception as e:
            print(f"⚠️  Could not retrieve project features: {e}")
        
        await mcp_client.close()
        
    except Exception as e:
        print(f"❌ Error connecting to Archon MCP server: {e}")
        return False
    
    return True

async def main():
    """Main function"""
    print("🚀 Archon MCP Status Check")
    print("=" * 50)
    
    success = await check_archon_status()
    
    if success:
        print("\n✅ Archon MCP connection test completed successfully")
    else:
        print("\n❌ Archon MCP connection test failed")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
