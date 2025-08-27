#!/usr/bin/env python3
"""
Test Configuration Loading

This script tests that the configuration system properly loads from config.json
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config import Config

def test_config_loading():
    """Test that configuration loads correctly from config.json"""
    print("🔍 Testing Configuration Loading...")
    
    try:
        # Create config instance (should auto-load config.json)
        config = Config()
        
        print("✅ Configuration loaded successfully")
        
        # Check that OpenAI API key is loaded
        if config.llm.openai_api_key:
            print(f"✅ OpenAI API key loaded: {config.llm.openai_api_key[:20]}...")
        else:
            print("❌ OpenAI API key not loaded")
            return False
        
        # Check other key settings
        print(f"✅ OpenAI model: {config.llm.openai_model}")
        print(f"✅ Ollama base URL: {config.llm.ollama_base_url}")
        print(f"✅ Ollama model: {config.llm.ollama_model}")
        print(f"✅ Max tokens: {config.llm.max_tokens}")
        print(f"✅ Temperature: {config.llm.temperature}")
        print(f"✅ Batch size: {config.processing.batch_size}")
        print(f"✅ Confidence threshold: {config.processing.confidence_threshold}")
        print(f"✅ Max daily cost: ${config.budget.max_daily_cost}")
        
        # Validate configuration
        if config.validate():
            print("✅ Configuration validation passed")
            return True
        else:
            print("❌ Configuration validation failed")
            return False
            
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False

def test_llm_engine_with_config():
    """Test that the LLM engine can use the loaded configuration"""
    print("\n🔍 Testing LLM Engine with Configuration...")
    
    try:
        from core.llm_engine import LLMEngine
        
        # Get config as dictionary for LLM engine
        config = Config()
        config_dict = config.get_full_config()
        
        # Create LLM engine with config
        engine = LLMEngine(config_dict)
        
        print("✅ LLM Engine created successfully with configuration")
        
        # Test a simple name parsing
        result = engine.parse_name(
            contact_name="TEST USER",
            customer_name="TEST COMPANY",
            email="test@example.com"
        )
        
        if result.success:
            print("✅ LLM Engine processing working with loaded config")
            print(f"📊 Result: {result.first_name} {result.last_name}")
            print(f"📊 Method: {result.processing_method}")
            return True
        else:
            print(f"❌ LLM Engine processing failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ LLM Engine test failed: {e}")
        return False

def main():
    """Run configuration tests"""
    print("🧪 Stuart Data Cleaning System - Configuration Test")
    print("=" * 60)
    
    results = []
    
    # Test configuration loading
    results.append(("Configuration Loading", test_config_loading()))
    
    # Test LLM engine with config
    results.append(("LLM Engine with Config", test_llm_engine_with_config()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All configuration tests passed!")
        return True
    else:
        print("⚠️  Some configuration tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
