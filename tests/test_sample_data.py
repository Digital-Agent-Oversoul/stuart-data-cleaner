#!/usr/bin/env python3
"""
Test script to validate core data processing functionality
"""

import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.data_processor import DataProcessor
from workflows.broadly_survey.survey_processor import SurveyProcessor
from workflows.contact_export.export_processor import ExportProcessor

def create_sample_data():
    """Create sample data for testing"""
    sample_data = pd.DataFrame({
        'contact_name': [
            'John Smith',
            'Jane Doe',
            'Bob Johnson',
            'Alice Brown',
            'Charlie Wilson'
        ],
        'email': [
            'john.smith@email.com',
            'jane.doe@email.com',
            'bob.johnson@email.com',
            'alice.brown@email.com',
            'charlie.wilson@email.com'
        ],
        'location': [
            'Dublin',
            'Milpitas',
            'Dublin',
            'Milpitas',
            'Dublin'
        ],
        'phone': [
            '555-0101',
            '555-0102',
            '555-0103',
            '555-0104',
            '555-0105'
        ]
    })
    return sample_data

def test_core_processing():
    """Test core data processing functionality"""
    print("🧪 Testing Core Data Processing...")
    
    # Create sample data
    sample_data = create_sample_data()
    print(f"📊 Sample data created: {len(sample_data)} records")
    
    # Test DataProcessor directly
    try:
        config = {
            'llm': {
                'openai_api_key': 'test',
                'openai_model': 'gpt-4o-mini'
            },
            'processing': {
                'batch_size': 10,
                'confidence_threshold': 0.3
            }
        }
        
        processor = DataProcessor(config)
        print("✅ DataProcessor initialized successfully")
        
        # Test survey processing
        survey_data = processor.process_survey_data(sample_data)
        print(f"✅ Survey processing completed: {len(survey_data)} records")
        
        # Test contact export processing
        export_data = processor.process_contact_export_data(sample_data)
        print(f"✅ Contact export processing completed: {len(export_data)} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Core processing test failed: {e}")
        return False

def test_workflow_processors():
    """Test workflow processors"""
    print("\n🔄 Testing Workflow Processors...")
    
    try:
        config = {
            'llm': {
                'openai_api_key': 'test',
                'openai_model': 'gpt-4o-mini'
            }
        }
        
        # Test SurveyProcessor
        survey_processor = SurveyProcessor(config)
        print("✅ SurveyProcessor initialized successfully")
        
        # Test ExportProcessor
        export_processor = ExportProcessor(config)
        print("✅ ExportProcessor initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow processor test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Stuart Data Cleaner - Core Functionality Test")
    print("=" * 50)
    
    # Test core processing
    core_success = test_core_processing()
    
    # Test workflow processors
    workflow_success = test_workflow_processors()
    
    print("\n📊 Test Results:")
    print(f"   Core Processing: {'✅ PASS' if core_success else '❌ FAIL'}")
    print(f"   Workflow Processors: {'✅ PASS' if workflow_success else '❌ FAIL'}")
    
    if core_success and workflow_success:
        print("\n🎉 All tests passed! Core functionality is working correctly.")
        print("   Ready to process real data files.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
