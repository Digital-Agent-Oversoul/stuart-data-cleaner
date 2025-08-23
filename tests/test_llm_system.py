#!/usr/bin/env python3
"""
Comprehensive LLM System Test

This script tests all three tiers of the LLM system:
1. OpenAI API (primary)
2. Ollama local LLM (fallback)
3. Rule-based processing (emergency fallback)
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.llm_engine import LLMEngine, OpenAIProcessor, OllamaProcessor, RuleBasedProcessor
from config.config import Config

def test_openai_processor():
    """Test OpenAI processor functionality"""
    print("🔍 Testing OpenAI Processor...")
    
    try:
        # Load configuration to get API key
        config = Config()
        
        if not config.llm.openai_api_key:
            print("  ⚠️  No OpenAI API key found in configuration")
            print("  📝 Add OpenAI API key to config/config.json")
            return False
        
        processor = OpenAIProcessor(
            api_key=config.llm.openai_api_key,
            model=config.llm.openai_model,
            max_tokens=config.llm.max_tokens,
            temperature=config.llm.temperature
        )
        
        # Test with a simple case
        result = processor.parse_name(
            contact_name="JOHN SMITH",
            customer_name="JOHN SMITH CORP",
            email="jsmith@email.com"
        )
        
        if result.success:
            print("  ✅ OpenAI processor working correctly")
            print(f"  📊 Result: {result.first_name} {result.last_name}")
            print(f"  📊 Confidence: {result.confidence}")
            print(f"  📊 Method: {result.processing_method}")
            return True
        else:
            print(f"  ❌ OpenAI processing failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"  ❌ OpenAI processor test failed: {e}")
        return False

def test_ollama_processor():
    """Test Ollama processor functionality"""
    print("\n🔍 Testing Ollama Processor...")
    
    try:
        processor = OllamaProcessor(
            base_url="http://localhost:11434",
            model="qwen2.5:7b-instruct-q4_K_M",
            max_tokens=150,
            temperature=0.1
        )
        
        # Test with a simple case
        result = processor.parse_name(
            contact_name="JANE DOE",
            customer_name="JANE DOE INC",
            email="jdoe@email.com"
        )
        
        if result.success:
            print("  ✅ Ollama processor working correctly")
            print(f"  📊 Result: {result.first_name} {result.last_name}")
            print(f"  📊 Confidence: {result.confidence}")
            print(f"  📊 Method: {result.processing_method}")
            return True
        else:
            print(f"  ❌ Ollama processing failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"  ❌ Ollama processor test failed: {e}")
        print("  📝 Make sure Ollama is running on http://localhost:11434")
        return False

def test_rule_based_processor():
    """Test rule-based processor functionality"""
    print("\n🔍 Testing Rule-Based Processor...")
    
    try:
        processor = RuleBasedProcessor()
        
        # Test with a simple case
        result = processor.parse_name(
            contact_name="BOB WILSON",
            customer_name="BOB WILSON LLC",
            email="bwilson@email.com"
        )
        
        if result.success:
            print("  ✅ Rule-based processor working correctly")
            print(f"  📊 Result: {result.first_name} {result.last_name}")
            print(f"  📊 Confidence: {result.confidence}")
            print(f"  📊 Method: {result.processing_method}")
            return True
        else:
            print(f"  ❌ Rule-based processing failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"  ❌ Rule-based processor test failed: {e}")
        return False

def test_unified_llm_engine():
    """Test the unified LLM engine with fallback system"""
    print("\n🔍 Testing Unified LLM Engine...")
    
    try:
        # Load configuration
        config = Config()
        test_config = config.get_full_config()
        
        engine = LLMEngine(test_config)
        
        # Test with a simple case
        result = engine.parse_name(
            contact_name="ALICE BROWN",
            customer_name="ALICE BROWN CO",
            email="abrown@email.com"
        )
        
        if result.success:
            print("  ✅ Unified LLM engine working correctly")
            print(f"  📊 Result: {result.first_name} {result.last_name}")
            print(f"  📊 Confidence: {result.confidence}")
            print(f"  📊 Method: {result.processing_method}")
            
            # Get processing statistics
            stats = engine.get_stats()
            print(f"  📊 Total records: {stats.total_records}")
            print(f"  📊 LLM processed: {stats.llm_processed}")
            print(f"  📊 Ollama fallback: {stats.ollama_fallback}")
            print(f"  📊 Rule-based fallback: {stats.rule_based_fallback}")
            print(f"  📊 Errors: {stats.errors}")
            
            return True
        else:
            print(f"  ❌ Unified LLM engine failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"  ❌ Unified LLM engine test failed: {e}")
        return False

def test_fallback_chain():
    """Test the complete fallback chain"""
    print("\n🔍 Testing Fallback Chain...")
    
    try:
        # Create config without OpenAI API key to force fallback
        fallback_config = {
            'openai': {
                'api_key': '',  # No API key to force fallback
                'model': 'gpt-4o-mini',
                'max_tokens': 150,
                'temperature': 0.1,
                'monthly_budget': 10.0,
                'alert_threshold': 0.8
            },
            'ollama': {
                'base_url': 'http://localhost:11434',
                'model': 'qwen2.5:7b-instruct-q4_K_M',
                'max_tokens': 150,
                'temperature': 0.1
            }
        }
        
        engine = LLMEngine(fallback_config)
        
        # Test with a simple case
        result = engine.parse_name(
            contact_name="CAROL DAVIS",
            customer_name="CAROL DAVIS GROUP",
            email="cdavis@example.com"
        )
        
        if result.success:
            print("  ✅ Fallback chain working correctly")
            print(f"  📊 Result: {result.first_name} {result.last_name}")
            print(f"  📊 Confidence: {result.confidence}")
            print(f"  📊 Method: {result.processing_method}")
            
            # Verify it used fallback method
            if result.processing_method in ['ollama', 'rule_based']:
                print("  ✅ Successfully fell back from OpenAI")
            else:
                print("  ⚠️  Unexpected processing method")
                
            return True
        else:
            print(f"  ❌ Fallback chain failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"  ❌ Fallback chain test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Stuart Data Cleaning System - LLM System Test")
    print("=" * 60)
    
    results = []
    
    # Test individual components
    results.append(("OpenAI Processor", test_openai_processor()))
    results.append(("Ollama Processor", test_ollama_processor()))
    results.append(("Rule-Based Processor", test_rule_based_processor()))
    
    # Test unified system
    results.append(("Unified LLM Engine", test_unified_llm_engine()))
    results.append(("Fallback Chain", test_fallback_chain()))
    
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
        print("🎉 All tests passed! The LLM system is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
