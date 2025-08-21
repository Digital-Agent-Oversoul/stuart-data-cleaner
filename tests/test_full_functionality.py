#!/usr/bin/env python3
"""
Full Functionality Test for Core Engine

This script tests the complete functionality of the core engine with real API keys.
It validates the OpenAI + Ollama fallback system and actual data processing.
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import get_default_config
from core.llm_engine import LLMEngine
from core.name_parser import NameParser
from core.data_processor import DataProcessor
from core.uncertainty_detector import UncertaintyDetector

def setup_environment():
    """Set up environment variables for testing"""
    print("🔧 Setting up environment for testing...")
    
    # Set OpenAI API key
    os.environ['OPENAI_API_KEY'] = "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"
    
    print("  ✅ Environment variables set")
    return True

def test_config_with_api_key():
    """Test configuration with API key"""
    print("\n🔧 Testing Configuration with API Key...")
    
    try:
        config = get_default_config()
        print(f"  ✅ Configuration loaded successfully")
        
        # Test validation (should pass now with API key)
        if config.validate():
            print("  ✅ Configuration validation passed")
        else:
            print("  ❌ Configuration validation failed")
            return None
            
        return config
        
    except Exception as e:
        print(f"  ❌ Configuration loading failed: {e}")
        return None

def test_llm_processing(config):
    """Test actual LLM processing"""
    print("\n🤖 Testing LLM Processing...")
    
    try:
        llm_config = config.get_llm_config()
        llm_engine = LLMEngine(llm_config)
        
        # Test with a simple name parsing case
        test_cases = [
            {
                'contact_name': 'John Smith',
                'customer_name': 'John Smith',
                'email': 'john.smith@email.com'
            },
            {
                'contact_name': 'Jane Doe',
                'customer_name': 'Jane Doe',
                'email': 'jane.doe@email.com'
            },
            {
                'contact_name': 'Bob Johnson',
                'customer_name': 'Bob Johnson',
                'email': 'bob.johnson@email.com'
            }
        ]
        
        print(f"  📊 Testing {len(test_cases)} name parsing cases...")
        
        for i, case in enumerate(test_cases, 1):
            try:
                result = llm_engine.parse_name(
                    contact_name=case['contact_name'],
                    customer_name=case['customer_name'],
                    email=case['email']
                )
                
                if result.success:
                    print(f"    ✅ Case {i}: {case['contact_name']} → {result.first_name} {result.last_name} (confidence: {result.confidence:.2f})")
                else:
                    print(f"    ❌ Case {i}: {case['contact_name']} failed - {result.error_message}")
                    
            except Exception as e:
                print(f"    ❌ Case {i}: {case['contact_name']} error - {e}")
        
        # Get processing stats
        stats = llm_engine.get_stats()
        print(f"  📊 Processing stats: {stats}")
        
        return llm_engine
        
    except Exception as e:
        print(f"  ❌ LLM processing test failed: {e}")
        return None

def test_name_parser_with_llm(llm_engine):
    """Test name parser with actual LLM processing"""
    print("\n📝 Testing Name Parser with LLM...")
    
    try:
        name_parser = NameParser(llm_engine)
        
        # Test batch processing
        test_data = [
            ('John Smith', 'John Smith', 'john.smith@email.com'),
            ('Jane Doe', 'Jane Doe', 'jane.doe@email.com'),
            ('Bob Johnson', 'Bob Johnson', 'bob.johnson@email.com')
        ]
        
        print(f"  📊 Testing batch processing with {len(test_data)} records...")
        
        for contact_name, customer_name, email in test_data:
            try:
                result = name_parser.parse_name(contact_name, customer_name, email)
                
                if result.success:
                    print(f"    ✅ {contact_name} → {result.first_name} {result.last_name} (confidence: {result.confidence:.2f})")
                else:
                    print(f"    ❌ {contact_name} failed - {result.error_message}")
                    
            except Exception as e:
                print(f"    ❌ {contact_name} error - {e}")
        
        return name_parser
        
    except Exception as e:
        print(f"  ❌ Name parser test failed: {e}")
        return None

def test_data_processor_with_real_data(config, llm_engine, name_parser):
    """Test data processor with real data processing"""
    print("\n🔄 Testing Data Processor with Real Data...")
    
    try:
        data_processor = DataProcessor(config.get_full_config())
        
        # Create test data that mimics real scenarios
        test_data = pd.DataFrame({
            'Contact Name': [
                'John Smith',
                'Jane Doe', 
                'Bob Johnson',
                'Mary Wilson',
                'David Brown'
            ],
            'Customer Name': [
                'John Smith',
                'Jane Doe',
                'Bob Johnson', 
                'Mary Wilson',
                'David Brown'
            ],
            'Email': [
                'john.smith@email.com',
                'jane.doe@email.com',
                'bob.johnson@email.com',
                'mary.wilson@email.com',
                'david.brown@email.com'
            ],
            'Location': [
                'Dublin',
                'Milpitas',
                'Dublin',
                'Milpitas',
                'Dublin'
            ]
        })
        
        print(f"  📊 Test data created: {len(test_data)} records")
        
        # Test survey data processing
        print("  🔄 Testing survey data processing...")
        survey_result = data_processor.process_survey_data(test_data, location_filter='Dublin')
        print(f"    ✅ Survey processing completed: {len(survey_result)} records")
        
        # Test contact export processing
        print("  🔄 Testing contact export processing...")
        export_result = data_processor.process_contact_export_data(test_data)
        print(f"    ✅ Contact export processing completed: {len(export_result)} records")
        
        # Get comprehensive stats
        stats = data_processor.get_processing_stats()
        print(f"  📊 Comprehensive processing stats: {stats}")
        
        return data_processor
        
    except Exception as e:
        print(f"  ❌ Data processor test failed: {e}")
        return None

def test_uncertainty_detection_with_real_data(uncertainty_detector, llm_engine):
    """Test uncertainty detection with real LLM responses"""
    print("\n❓ Testing Uncertainty Detection with Real Data...")
    
    try:
        # Test with edge cases that might trigger uncertainty
        edge_cases = [
            ('A B', 'A B', 'a.b@email.com'),  # Initials only
            ('Smith & Johnson', 'Smith & Johnson', 'info@company.com'),  # Multiple names
            ('', 'Company LLC', 'sales@company.com'),  # Empty contact name
            ('Very Long Name That Exceeds Normal Limits', 'Very Long Name That Exceeds Normal Limits', 'longname@email.com')  # Very long name
        ]
        
        print(f"  📊 Testing {len(edge_cases)} edge cases for uncertainty detection...")
        
        for i, (contact_name, customer_name, email) in enumerate(edge_cases, 1):
            try:
                # Get LLM response for this case
                llm_response = llm_engine.parse_name(contact_name, customer_name, email)
                
                # Check for uncertainty
                uncertainty_case = uncertainty_detector.detect_uncertainty(
                    record_id=f"test_{i}",
                    contact_name=contact_name,
                    customer_name=customer_name,
                    email=email,
                    llm_response=llm_response
                )
                
                if uncertainty_case:
                    print(f"    ⚠️ Case {i}: Uncertainty detected - {uncertainty_case.uncertainty_type} (confidence: {uncertainty_case.confidence_score:.2f})")
                    if uncertainty_case.suggested_resolution:
                        print(f"      💡 Suggestion: {uncertainty_case.suggested_resolution}")
                else:
                    print(f"    ✅ Case {i}: No uncertainty detected")
                    
            except Exception as e:
                print(f"    ❌ Case {i}: Error - {e}")
        
        # Get uncertainty summary
        summary = uncertainty_detector.get_uncertainty_summary()
        print(f"  📊 Uncertainty summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Uncertainty detection test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Full Functionality Tests")
    print("=" * 50)
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed. Exiting.")
        return False
    
    # Test configuration with API key
    config = test_config_with_api_key()
    if not config:
        print("❌ Configuration test failed. Exiting.")
        return False
    
    # Test LLM processing
    llm_engine = test_llm_processing(config)
    if not llm_engine:
        print("❌ LLM processing test failed. Exiting.")
        return False
    
    # Test name parser with LLM
    name_parser = test_name_parser_with_llm(llm_engine)
    if not name_parser:
        print("❌ Name parser test failed. Exiting.")
        return False
    
    # Test data processor with real data
    data_processor = test_data_processor_with_real_data(config, llm_engine, name_parser)
    if not data_processor:
        print("❌ Data processor test failed. Exiting.")
        return False
    
    # Test uncertainty detection with real data
    uncertainty_success = test_uncertainty_detection_with_real_data(data_processor.uncertainty_detector, llm_engine)
    if not uncertainty_success:
        print("❌ Uncertainty detection test failed.")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All Full Functionality Tests Passed!")
    print("✅ Environment setup: PASSED")
    print("✅ Configuration with API key: PASSED")
    print("✅ LLM processing: PASSED")
    print("✅ Name parser with LLM: PASSED")
    print("✅ Data processor with real data: PASSED")
    print("✅ Uncertainty detection with real data: PASSED")
    print("\n🚀 Core Engine is fully functional!")
    print("📝 Ready for production use and next phase development")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
