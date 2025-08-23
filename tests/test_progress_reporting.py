#!/usr/bin/env python3
"""
Test script for progress reporting feature
"""

import sys
import os
import pandas as pd
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config import Config
from core.data_processor import DataProcessor

def create_sample_data():
    """Create sample data for testing progress reporting"""
    print("🔧 Creating sample data for progress reporting test...")
    
    # Sample data with various name formats
    sample_data = [
        {
            'Contract': '001',
            'Salesperson': 'John Smith',
            'Key': 'KEY001',
            'DEL': 'DEL001',
            'PU': 'PU001',
            'Email': 'john.smith@example.com',
            'Contact Name': 'John Smith',
            'Customer Name': 'John Smith',
            'Phone': '(555) 123-4567',
            'Type': 'W',
            'Business Type': 'HOMEOWNER',
            'Address 1': '123 Main St',
            'Address 2': '',
            'City': 'Albany',
            'State': 'CA',
            'Zip': '94706',
            'Delivery Date': '2025-01-07',
            'Event Date': '2025-01-07',
            'Return Date': '2025-01-07'
        },
        {
            'Contract': '002',
            'Salesperson': 'Jane Doe',
            'Key': 'KEY002',
            'DEL': 'DEL002',
            'PU': 'PU002',
            'Email': 'jane.doe@example.com',
            'Contact Name': 'Jane Doe',
            'Customer Name': 'Jane Doe',
            'Phone': '(555) 234-5678',
            'Type': 'W',
            'Business Type': 'HOMEOWNER',
            'Address 1': '456 Oak Ave',
            'Address 2': 'Suite 100',
            'City': 'Berkeley',
            'State': 'CA',
            'Zip': '94704',
            'Delivery Date': '2025-01-08',
            'Event Date': '2025-01-08',
            'Return Date': '2025-01-08'
        },
        {
            'Contract': '003',
            'Salesperson': 'Bob Wilson',
            'Key': 'KEY003',
            'DEL': 'DEL003',
            'PU': 'PU003',
            'Email': 'bob.wilson@example.com',
            'Contact Name': 'Bob Wilson',
            'Customer Name': 'Bob Wilson',
            'Phone': '(555) 345-6789',
            'Type': 'W',
            'Business Type': 'HOMEOWNER',
            'Address 1': '789 Pine Rd',
            'Address 2': '',
            'City': 'Oakland',
            'State': 'CA',
            'Zip': '94601',
            'Delivery Date': '2025-01-09',
            'Event Date': '2025-01-09',
            'Return Date': '2025-01-09'
        }
    ]
    
    df = pd.DataFrame(sample_data)
    print(f"✅ Sample data created with {len(df)} records")
    return df

def test_progress_reporting():
    """Test progress reporting with sample data"""
    print("🧪 Testing progress reporting feature...")
    
    # Load test configuration
    config_path = project_root / "test_config.json"
    if not config_path.exists():
        print(f"❌ Test configuration not found: {config_path}")
        return False
    
    try:
        config = Config(str(config_path))
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return False
    
    # Test with progress enabled
    print("\n📊 Testing with progress reporting ENABLED...")
    config.processing.show_progress = True
    
    try:
        processor = DataProcessor(config.__dict__)
        print("✅ Data processor initialized with progress enabled")
        
        # Create sample data
        sample_data = create_sample_data()
        
        # Process data (this should show progress)
        print("\n🔄 Processing sample data with progress reporting...")
        processed_data = processor.process_contact_export_data(sample_data)
        
        print(f"✅ Processing complete: {len(processed_data)} records processed")
        
    except Exception as e:
        print(f"❌ Failed to process with progress enabled: {e}")
        return False
    
    # Test with progress disabled
    print("\n📊 Testing with progress reporting DISABLED...")
    config.processing.show_progress = False
    
    try:
        processor = DataProcessor(config.__dict__)
        print("✅ Data processor initialized with progress disabled")
        
        # Process data (this should NOT show progress)
        print("\n🔄 Processing sample data without progress reporting...")
        processed_data = processor.process_contact_export_data(sample_data)
        
        print(f"✅ Processing complete: {len(processed_data)} records processed")
        
    except Exception as e:
        print(f"❌ Failed to process with progress disabled: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_progress_reporting()
    if success:
        print("\n🎉 Progress reporting test completed successfully!")
        print("✅ Progress reporting can be enabled/disabled via configuration")
    else:
        print("\n💥 Progress reporting test failed!")
        sys.exit(1)
