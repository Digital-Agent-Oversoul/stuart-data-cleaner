#!/usr/bin/env python3
"""
Basic Integration Test for Core Engine

This script tests the basic integration of core modules without requiring API keys.
It validates the structure and initialization of all components.
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

def test_config_loading():
    """Test configuration loading and validation"""
    print("🔧 Testing Configuration Loading...")
    
    try:
        config = get_default_config()
        print(f"  ✅ Configuration loaded successfully")
        print(f"  📊 LLM Model: {config.llm.openai_model}")
        print(f"  📊 Ollama Model: {config.llm.ollama_model}")
        print(f"  📊 Batch Size: {config.processing.batch_size}")
        print(f"  📊 Confidence Threshold: {config.processing.confidence_threshold}")
        
        # Test validation (will fail without API key, but that's expected)
        if config.validate():
            print("  ✅ Configuration validation passed")
        else:
            print("  ⚠️ Configuration validation failed (expected without API key)")
            
        return config
        
    except Exception as e:
        print(f"  ❌ Configuration loading failed: {e}")
        return None

def test_llm_engine_initialization(config):
    """Test LLM engine initialization"""
    print("\n🤖 Testing LLM Engine Initialization...")
    
    try:
        llm_config = config.get_llm_config()
        llm_engine = LLMEngine(llm_config)
        print("  ✅ LLM Engine initialized successfully")
        print(f"  📊 Total records processed: {llm_engine.get_stats().total_records}")
        return llm_engine
        
    except Exception as e:
        print(f"  ❌ LLM Engine initialization failed: {e}")
        return None

def test_name_parser_initialization(llm_engine):
    """Test name parser initialization"""
    print("\n📝 Testing Name Parser Initialization...")
    
    try:
        name_parser = NameParser(llm_engine)
        print("  ✅ Name Parser initialized successfully")
        return name_parser
        
    except Exception as e:
        print(f"  ❌ Name Parser initialization failed: {e}")
        return None

def test_data_processor_initialization(config, llm_engine, name_parser):
    """Test data processor initialization"""
    print("\n🔄 Testing Data Processor Initialization...")
    
    try:
        data_processor = DataProcessor(config.get_full_config())
        print("  ✅ Data Processor initialized successfully")
        print(f"  📊 Processing stats: {data_processor.get_processing_stats()}")
        return data_processor
        
    except Exception as e:
        print(f"  ❌ Data Processor initialization failed: {e}")
        return None

def test_uncertainty_detector_initialization(config):
    """Test uncertainty detector initialization"""
    print("\n❓ Testing Uncertainty Detector Initialization...")
    
    try:
        uncertainty_detector = UncertaintyDetector(config.get_uncertainty_config())
        print("  ✅ Uncertainty Detector initialized successfully")
        print(f"  📊 Low confidence threshold: {uncertainty_detector.low_confidence_threshold}")
        print(f"  📊 Very low confidence threshold: {uncertainty_detector.very_low_confidence_threshold}")
        return uncertainty_detector
        
    except Exception as e:
        print(f"  ❌ Uncertainty Detector initialization failed: {e}")
        return None

def test_sample_data_creation():
    """Test creating sample data without processing"""
    print("\n📊 Testing Sample Data Creation...")
    
    try:
        # Create sample data
        sample_data = pd.DataFrame({
            'Contact Name': ['John Smith', 'Jane Doe', 'Bob Johnson'],
            'Customer Name': ['John Smith', 'Jane Doe', 'Bob Johnson'],
            'Email': ['john.smith@email.com', 'jane.doe@email.com', 'bob.johnson@email.com'],
            'Location': ['Dublin', 'Milpitas', 'Dublin']
        })
        
        print(f"  ✅ Sample data created: {len(sample_data)} records")
        print(f"  📊 Columns: {list(sample_data.columns)}")
        print(f"  📊 Sample row: {sample_data.iloc[0].to_dict()}")
        
        return sample_data
        
    except Exception as e:
        print(f"  ❌ Sample data creation failed: {e}")
        return None

def test_uncertainty_detection(uncertainty_detector):
    """Test uncertainty detection functionality"""
    print("\n❓ Testing Uncertainty Detection...")
    
    try:
        # Test business indicators loading
        business_indicators = uncertainty_detector.business_indicators
        print(f"  ✅ Business indicators loaded: {len(business_indicators)} patterns")
        
        # Test edge case patterns loading
        edge_case_patterns = uncertainty_detector.edge_case_patterns
        print(f"  ✅ Edge case patterns loaded: {len(edge_case_patterns)} patterns")
        
        # Test uncertainty summary
        summary = uncertainty_detector.get_uncertainty_summary()
        print(f"  ✅ Uncertainty summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Uncertainty detection testing failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Basic Core Engine Integration Tests")
    print("=" * 50)
    
    # Test configuration
    config = test_config_loading()
    if not config:
        print("❌ Configuration test failed. Exiting.")
        return False
    
    # Test LLM engine
    llm_engine = test_llm_engine_initialization(config)
    if not llm_engine:
        print("❌ LLM Engine test failed. Exiting.")
        return False
    
    # Test name parser
    name_parser = test_name_parser_initialization(llm_engine)
    if not name_parser:
        print("❌ Name Parser test failed. Exiting.")
        return False
    
    # Test data processor
    data_processor = test_data_processor_initialization(config, llm_engine, name_parser)
    if not data_processor:
        print("❌ Data Processor test failed. Exiting.")
        return False
    
    # Test uncertainty detector
    uncertainty_detector = test_uncertainty_detector_initialization(config)
    if not uncertainty_detector:
        print("❌ Uncertainty Detector test failed. Exiting.")
        return False
    
    # Test sample data creation
    sample_data = test_sample_data_creation()
    if sample_data is None:
        print("❌ Sample data creation test failed.")
        return False
    
    # Test uncertainty detection
    uncertainty_success = test_uncertainty_detection(uncertainty_detector)
    if not uncertainty_success:
        print("❌ Uncertainty detection test failed.")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All Basic Core Engine Integration Tests Passed!")
    print("✅ Configuration loading: PASSED")
    print("✅ LLM Engine initialization: PASSED")
    print("✅ Name Parser initialization: PASSED")
    print("✅ Data Processor initialization: PASSED")
    print("✅ Uncertainty Detector initialization: PASSED")
    print("✅ Sample data creation: PASSED")
    print("✅ Uncertainty detection: PASSED")
    print("\n🚀 Core Engine structure is ready!")
    print("📝 Next step: Test with real API keys for full functionality")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
