#!/usr/bin/env python3
"""
OpenAI Integration Test Script for Stuart Data Cleaner

This script tests the Contact Export workflow with OpenAI integration
and monitors API usage costs.
"""

import json
import sys
import os
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def load_config():
    """Load test configuration"""
    config_file = project_root / "test_config.json"
    with open(config_file, 'r') as f:
        return json.load(f)

def test_openai_integration():
    """Test OpenAI integration with Contact Export workflow"""
    print("🚀 Starting OpenAI Integration Test")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    print(f"✅ Configuration loaded")
    print(f"   OpenAI Model: {config['openai']['model']}")
    print(f"   Batch size: {config['processing']['batch_size']}")
    print(f"   Monthly budget: ${config['openai']['monthly_budget']}")
    
    # Test OpenAI API connection
    try:
        import openai
        openai.api_key = config['openai']['api_key']
        
        # Test API connection with a simple request
        print("\n🧪 Testing OpenAI API connection...")
        response = openai.chat.completions.create(
            model=config['openai']['model'],
            messages=[{"role": "user", "content": "Hello, this is a test message."}],
            max_tokens=10,
            temperature=0
        )
        print(f"✅ OpenAI API connection successful!")
        print(f"   Response: {response.choices[0].message.content}")
        print(f"   Usage: {response.usage}")
        
        # Calculate cost (gpt-4o-mini: $0.15 per 1M tokens)
        total_tokens = response.usage.total_tokens
        cost = (total_tokens / 1000000) * 0.15
        print(f"   Cost: ${cost:.6f}")
        
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")
        return False
    
    # Test data loading
    try:
        print("\n📊 Testing data loading...")
        import pandas as pd
        
        # Load the small dataset
        data_file = r"C:\LocalAI\!projects\Stuart\Broadly Report\Broadly RAW\Broadly - 7.29.25-8.04.25 - RawData.xlsx"
        df = pd.read_excel(data_file)
        
        # Clean the data (remove empty rows, get actual data)
        df_clean = df.dropna(how='all')
        df_data = df_clean.iloc[1:]  # Skip header row
        
        # Apply correct column mapping
        df_mapped = df_data.copy()
        df_mapped['contact_name'] = df_data['Unnamed: 6']  # Contact Name column
        df_mapped['customer_name'] = df_data['Unnamed: 7']  # Customer Name column  
        df_mapped['email'] = df_data['Unnamed: 5']          # Email column
        
        print(f"✅ Data loaded successfully!")
        print(f"   Total rows: {len(df)}")
        print(f"   Clean rows: {len(df_data)}")
        print(f"   Mapped columns: contact_name, customer_name, email")
        
        # Show sample data with correct mapping
        print(f"\n📋 Sample data (with correct mapping):")
        sample_data = df_mapped.head(3)
        for idx, row in sample_data.iterrows():
            contact_name = row.get('contact_name', 'N/A')
            customer_name = row.get('customer_name', 'N/A')
            email = row.get('email', 'N/A')
            print(f"   Row {idx}: Contact='{contact_name}', Customer='{customer_name}', Email='{email}'")
        
    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        return False
    
    # Test Contact Export workflow
    try:
        print("\n🔄 Testing Contact Export workflow...")
        
        # Import the workflow processor
        from workflows.contact_export.export_processor import ExportProcessor
        
        # Initialize processor
        processor = ExportProcessor(config)
        print(f"✅ ExportProcessor initialized")
        
        # Process a small sample for testing
        test_data = df_mapped.head(5)  # Test with first 5 rows
        print(f"   Processing {len(test_data)} test records...")
        
        # Start timing
        start_time = time.time()
        
        # Process the data
        processed_data = processor.process_contact_export(test_data)
        
        # End timing
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Processing completed!")
        print(f"   Time: {processing_time:.2f} seconds")
        print(f"   Records processed: {len(processed_data)}")
        
        # Save test output
        output_file = project_root / "test_output" / f"test_contact_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        processed_data.to_excel(output_file, index=False)
        print(f"   Output saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Contact Export workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 Stuart Data Cleaner - OpenAI Integration Test")
    print("=" * 60)
    
    # Run the test
    success = test_openai_integration()
    
    if success:
        print("\n🎉 All tests passed! OpenAI integration is working correctly.")
        print("   Ready for full dataset processing.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
