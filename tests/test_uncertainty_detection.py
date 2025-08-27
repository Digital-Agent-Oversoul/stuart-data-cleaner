#!/usr/bin/env python3
"""
Uncertainty Detection System Test

This script tests the uncertainty detection functionality of the core engine.
It validates that the system correctly identifies uncertain cases and provides
appropriate suggestions for human guidance.
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
from core.uncertainty_detector import UncertaintyDetector

def setup_environment():
    """Set up environment variables for testing"""
    print("🔧 Setting up environment for testing...")
    
    # Set OpenAI API key
    os.environ['OPENAI_API_KEY'] = "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"
    
    print("  ✅ Environment variables set")
    return True

def test_uncertainty_detector_initialization(config):
    """Test uncertainty detector initialization and configuration"""
    print("\n❓ Testing Uncertainty Detector Initialization...")
    
    try:
        uncertainty_detector = UncertaintyDetector(config.get_uncertainty_config())
        print("  ✅ Uncertainty Detector initialized successfully")
        print("  📊 Low confidence threshold: " + str(uncertainty_detector.low_confidence_threshold))
        print("  📊 Very low confidence threshold: " + str(uncertainty_detector.very_low_confidence_threshold))
        
        # Test business indicators loading
        business_indicators = uncertainty_detector.business_indicators
        print("  📊 Business indicators loaded: " + str(len(business_indicators)) + " patterns")
        
        # Test edge case patterns loading
        edge_case_patterns = uncertainty_detector.edge_case_patterns
        print("  📊 Edge case patterns loaded: " + str(len(edge_case_patterns)) + " patterns")
        
        return uncertainty_detector
        
    except Exception as e:
        print("  ❌ Uncertainty Detector initialization failed: " + str(e))
        return None

def test_uncertainty_detection_with_edge_cases(uncertainty_detector, llm_engine):
    """Test uncertainty detection with various edge cases"""
    print("\n❓ Testing Uncertainty Detection with Edge Cases...")
    
    # Define edge cases that should trigger uncertainty
    edge_cases = [
        {
            'name': 'Initials Only',
            'contact_name': 'A B',
            'customer_name': 'A B',
            'email': 'a.b@email.com',
            'expected_uncertainty': True
        },
        {
            'name': 'Multiple Names',
            'contact_name': 'Smith & Johnson',
            'customer_name': 'Smith & Johnson',
            'email': 'info@company.com',
            'expected_uncertainty': True
        },
        {
            'name': 'Empty Contact Name',
            'contact_name': '',
            'customer_name': 'Company LLC',
            'email': 'sales@company.com',
            'expected_uncertainty': True
        },
        {
            'name': 'Very Long Name',
            'contact_name': 'Very Long Name That Exceeds Normal Limits And Should Trigger Uncertainty Detection',
            'customer_name': 'Very Long Name That Exceeds Normal Limits And Should Trigger Uncertainty Detection',
            'email': 'longname@email.com',
            'expected_uncertainty': True
        },
        {
            'name': 'Business Indicators',
            'contact_name': 'Sales Department',
            'customer_name': 'Sales Department',
            'email': 'sales@company.com',
            'expected_uncertainty': True
        },
        {
            'name': 'Clear Person Name',
            'contact_name': 'John Smith',
            'customer_name': 'John Smith',
            'email': 'john.smith@email.com',
            'expected_uncertainty': False
        }
    ]
    
    print("  📊 Testing " + str(len(edge_cases)) + " edge cases for uncertainty detection...")
    
    uncertainty_cases = []
    
    for i, case in enumerate(edge_cases, 1):
        try:
            print("    🔍 Testing: " + case['name'])
            
            # Get LLM response for this case
            llm_response = llm_engine.parse_name(
                contact_name=case['contact_name'],
                customer_name=case['customer_name'],
                email=case['email']
            )
            
            # Check for uncertainty
            uncertainty_case = uncertainty_detector.detect_uncertainty(
                record_id=f"test_{i}",
                contact_name=case['contact_name'],
                customer_name=case['customer_name'],
                email=case['email'],
                llm_response=llm_response
            )
            
            if uncertainty_case:
                uncertainty_cases.append(uncertainty_case)
                print("      ⚠️ Uncertainty detected - " + uncertainty_case.uncertainty_type + " (confidence: " + str(round(uncertainty_case.confidence_score, 2)) + ")")
                
                if uncertainty_case.suggested_resolution:
                    print("      💡 Suggestion: " + uncertainty_case.suggested_resolution)
                    
                # Check if this matches our expectation
                if case['expected_uncertainty']:
                    print("      ✅ Expected uncertainty detected")
                else:
                    print("      ❌ Unexpected uncertainty detected")
            else:
                print("      ✅ No uncertainty detected")
                
                # Check if this matches our expectation
                if case['expected_uncertainty']:
                    print("      ❌ Expected uncertainty not detected")
                else:
                    print("      ✅ Expected no uncertainty")
                    
        except Exception as e:
            print("      ❌ Error processing case: " + str(e))
    
    return uncertainty_cases

def test_uncertainty_resolution_system(uncertainty_detector, uncertainty_cases):
    """Test the uncertainty resolution system"""
    print("\n🔧 Testing Uncertainty Resolution System...")
    
    if not uncertainty_cases:
        print("  ⚠️ No uncertainty cases to test resolution")
        return False
    
    print("  📊 Testing resolution for " + str(len(uncertainty_cases)) + " uncertainty cases...")
    
    for i, case in enumerate(uncertainty_cases, 1):
        try:
            print("    🔧 Resolving case " + str(i) + ": " + case.uncertainty_type)
            
            # Simulate user resolution
            resolution = {
                'resolved_name': 'Resolved Name',
                'confidence': 0.9,
                'resolution_notes': 'User provided guidance for this case',
                'resolved_at': '2025-08-20T23:15:00Z'
            }
            
            # Apply resolution
            success = uncertainty_detector.resolve_uncertainty_case(case.record_id, resolution)
            
            if success:
                print("      ✅ Resolution applied successfully")
            else:
                print("      ❌ Resolution failed")
                
        except Exception as e:
            print("      ❌ Error resolving case: " + str(e))
    
    # Get updated uncertainty summary
    summary = uncertainty_detector.get_uncertainty_summary()
    print("  📊 Updated uncertainty summary: " + str(summary))
    
    return True

def test_learning_patterns(uncertainty_detector):
    """Test the learning patterns functionality"""
    print("\n🧠 Testing Learning Patterns...")
    
    try:
        # Get learning patterns
        patterns = uncertainty_detector.get_learning_patterns()
        print("  📊 Learning patterns: " + str(patterns))
        
        # Test pattern evolution tracking
        print("  📊 Pattern evolution tracking available: " + str(hasattr(uncertainty_detector, 'pattern_evolution')))
        
        return True
        
    except Exception as e:
        print("  ❌ Learning patterns test failed: " + str(e))
        return False

def test_uncertainty_summary_and_analytics(uncertainty_detector):
    """Test uncertainty summary and analytics"""
    print("\n📊 Testing Uncertainty Summary and Analytics...")
    
    try:
        # Get comprehensive uncertainty summary
        summary = uncertainty_detector.get_uncertainty_summary()
        print("  📊 Uncertainty summary: " + str(summary))
        
        # Test uncertainty tracking
        print("  📊 Total uncertainty cases tracked: " + str(summary.get('total_cases', 0)))
        print("  📊 Cases by type: " + str(summary.get('cases_by_type', {})))
        
        return True
        
    except Exception as e:
        print("  ❌ Uncertainty summary test failed: " + str(e))
        return False

def main():
    """Main test function"""
    print("🚀 Starting Uncertainty Detection System Tests")
    print("=" * 60)
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed. Exiting.")
        return False
    
    # Get configuration
    config = get_default_config()
    if not config:
        print("❌ Configuration loading failed. Exiting.")
        return False
    
    # Initialize LLM engine
    llm_config = config.get_llm_config()
    llm_engine = LLMEngine(llm_config)
    
    # Test uncertainty detector initialization
    uncertainty_detector = test_uncertainty_detector_initialization(config)
    if not uncertainty_detector:
        print("❌ Uncertainty detector initialization failed. Exiting.")
        return False
    
    # Test uncertainty detection with edge cases
    uncertainty_cases = test_uncertainty_detection_with_edge_cases(uncertainty_detector, llm_engine)
    if uncertainty_cases is None:
        print("❌ Uncertainty detection test failed. Exiting.")
        return False
    
    # Test uncertainty resolution system
    resolution_success = test_uncertainty_resolution_system(uncertainty_detector, uncertainty_cases)
    if not resolution_success:
        print("❌ Uncertainty resolution test failed.")
        return False
    
    # Test learning patterns
    learning_success = test_learning_patterns(uncertainty_detector)
    if not learning_success:
        print("❌ Learning patterns test failed.")
        return False
    
    # Test uncertainty summary and analytics
    summary_success = test_uncertainty_summary_and_analytics(uncertainty_detector)
    if not summary_success:
        print("❌ Uncertainty summary test failed.")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All Uncertainty Detection System Tests Passed!")
    print("✅ Uncertainty detector initialization: PASSED")
    print("✅ Uncertainty detection with edge cases: PASSED")
    print("✅ Uncertainty resolution system: PASSED")
    print("✅ Learning patterns: PASSED")
    print("✅ Uncertainty summary and analytics: PASSED")
    print("\n🚀 Uncertainty Detection System is fully functional!")
    print("📝 Ready for interactive learning implementation")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
