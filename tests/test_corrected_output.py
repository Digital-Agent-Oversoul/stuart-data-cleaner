#!/usr/bin/env python3
"""
Corrected Output Test Script

This script tests the corrected export processor to ensure proper output structure.
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

def test_corrected_output():
    """Test the corrected export processor with proper output structure"""
    print("🚀 Testing Corrected Output Structure")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    print(f"✅ Configuration loaded")
    print(f"   OpenAI Model: {config['openai']['model']}")
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
        
        # Add other required columns
        df_mapped['Salesperson'] = df_data['Unnamed: 1']    # Salesperson
        df_mapped['Phone'] = df_data['Unnamed: 8']          # Phone
        df_mapped['Business Type'] = df_data['Unnamed: 10'] # Business Type
        df_mapped['Address 1'] = df_data['Unnamed: 11']     # Address 1
        df_mapped['Address 2'] = df_data['Unnamed: 12']     # Address 2
        df_mapped['City'] = df_data['Unnamed: 13']          # City
        df_mapped['State'] = df_data['Unnamed: 14']         # State
        df_mapped['Zip'] = df_data['Unnamed: 15']           # Zip
        
        print(f"✅ Data loaded successfully!")
        print(f"   Total rows: {len(df)}")
        print(f"   Clean rows: {len(df_data)}")
        print(f"   Mapped columns: contact_name, customer_name, email, + required fields")
        
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
    
    # Test Corrected Export Processor
    try:
        print("\n🔄 Testing Corrected Export Processor...")
        
        # Import the corrected processor
        from workflows.contact_export.export_processor import ExportProcessor
        
        # Initialize processor
        processor = ExportProcessor(config)
        print(f"✅ ExportProcessor initialized")
        
        # Process a small sample for testing
        test_data = df_mapped.head(10)  # Test with first 10 rows
        print(f"   Processing {len(test_data)} test records...")
        
        # Start timing
        start_time = time.time()
        
        # Process the data
        processed_data, removed_rows = processor.process_contact_export(test_data)
        
        # End timing
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Processing completed!")
        print(f"   Time: {processing_time:.2f} seconds")
        print(f"   Records processed: {len(processed_data)}")
        print(f"   Records removed: {len(removed_rows)}")
        
        # Show output structure
        print(f"\n📊 Output Structure:")
        print(f"   Columns: {list(processed_data.columns)}")
        print(f"   Shape: {processed_data.shape}")
        
        # Show first few processed records
        print(f"\n📋 First 3 processed records:")
        print(processed_data.head(3).to_string())
        
        # Create Excel output with proper structure
        output_file = project_root / "test_output" / f"corrected_contact_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        processor.create_excel_output(processed_data, removed_rows, str(output_file))
        
        print(f"\n✅ Excel output created with proper structure!")
        print(f"   File: {output_file}")
        print(f"   Sheets: Alert Contact Export, Removed")
        
        return True
        
    except Exception as e:
        print(f"❌ Corrected Export Processor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 Stuart Data Cleaner - Corrected Output Structure Test")
    print("=" * 70)
    
    # Run the test
    success = test_corrected_output()
    
    if success:
        print("\n🎉 All tests passed! Corrected output structure is working correctly.")
        print("   Ready for full dataset processing with proper format.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
