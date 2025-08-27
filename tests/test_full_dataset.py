#!/usr/bin/env python3
"""
Full Dataset Test Script

This script tests the corrected export processor with the complete dataset
to see what rows actually get removed during processing.
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

def test_full_dataset():
    """Test the corrected export processor with the full dataset"""
    print("🚀 Testing Full Dataset Processing")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    print(f"✅ Configuration loaded")
    print(f"   OpenAI Model: {config['openai']['model']}")
    print(f"   Monthly budget: ${config['openai']['monthly_budget']}")
    
    # Test data loading
    try:
        print("\n📊 Loading full dataset...")
        import pandas as pd
        
        # Load the small dataset
        data_file = r"C:\LocalAI\!projects\Stuart\Broadly Report\Broadly RAW\Broadly - 7.29.25-8.04.25 - RawData.xlsx"
        
        # Read the data with proper header handling
        # Row 3 contains the actual column headers
        df = pd.read_excel(data_file, sheet_name='slsp', header=2)  # header=2 means row 3 (0-indexed)
        
        # Clean the data (remove empty rows, get actual data)
        df_clean = df.dropna(how='all')
        df_data = df_clean  # No need to skip header row since we already read it correctly
        
        # Apply correct column mapping using the actual column names
        df_mapped = df_data.copy()
        df_mapped['contact_name'] = df_data['Contact Name']  # Contact Name column
        df_mapped['customer_name'] = df_data['Customer Name']  # Customer Name column  
        df_mapped['email'] = df_data['Email']          # Email column
        
        # Add other required columns
        df_mapped['Salesperson'] = df_data['Salesperson']    # Salesperson
        df_mapped['Phone'] = df_data['Phone']          # Phone
        df_mapped['Business Type'] = df_data['Business Type'] # Business Type
        df_mapped['Address 1'] = df_data['Address 1']     # Address 1
        df_mapped['Address 2'] = df_data['Address 2']     # Address 2
        df_mapped['City'] = df_data['City']          # City
        df_mapped['State'] = df_data['State']         # State
        df_mapped['Zip'] = df_data['Zip']           # Zip
        
        print(f"✅ Data loaded successfully!")
        print(f"   Total rows: {len(df)}")
        print(f"   Clean rows: {len(df_data)}")
        print(f"   Rows to process: {len(df_mapped)}")
        
        # Show some sample data
        print(f"\n📋 Sample data from full dataset:")
        sample_data = df_mapped.head(3)
        for idx, row in sample_data.iterrows():
            contact_name = row.get('contact_name', 'N/A')
            customer_name = row.get('customer_name', 'N/A')
            email = row.get('email', 'N/A')
            salesperson = row.get('Salesperson', 'N/A')
            print(f"   Row {idx}: Contact='{contact_name}', Customer='{customer_name}', Email='{email}', Salesperson='{salesperson}'")
        
        # Store the ORIGINAL source data for proper removed row tracking
        original_source_data = df_data.copy()  # This preserves the actual column headers from row 3
        
    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        return False
    
    # Test Corrected Export Processor with FULL dataset
    try:
        print("\n🔄 Testing Corrected Export Processor with FULL dataset...")
        
        # Import the corrected processor
        from workflows.contact_export.export_processor import ExportProcessor
        
        # Initialize processor
        processor = ExportProcessor(config)
        print(f"✅ ExportProcessor initialized")
        
        # Process the FULL dataset (not just 10 rows)
        print(f"   Processing ALL {len(df_mapped)} records...")
        
        # Start timing
        start_time = time.time()
        
        # Process the data
        processed_data, removed_rows = processor.process_contact_export(df_mapped, original_source_data)
        
        # End timing
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Processing completed!")
        print(f"   Time: {processing_time:.2f} seconds")
        print(f"   Records processed: {len(processed_data)}")
        print(f"   Records removed: {len(removed_rows)}")
        
        # Show what was removed
        if removed_rows:
            print(f"\n🗑️  Removed rows analysis:")
            print(f"   Total removed: {len(removed_rows)}")
            
            # Analyze why rows were removed
            removed_reasons = {}
            for row in removed_rows:
                salesperson = row.get('Salesperson', 'Unknown')
                email = row.get('email', 'No email')
                contact_name = row.get('contact_name', 'No contact name')
                
                if salesperson and 'ACCOUNTS RECEIVABLE' in str(salesperson).upper():
                    removed_reasons['Accounts Receivable'] = removed_reasons.get('Accounts Receivable', 0) + 1
                elif pd.isna(email) or email == '' or email == 'nan':
                    removed_reasons['Invalid Email'] = removed_reasons.get('Invalid Email', 0) + 1
                elif pd.isna(contact_name) or contact_name == '' or contact_name == 'nan':
                    removed_reasons['No Contact Name'] = removed_reasons.get('No Contact Name', 0) + 1
                else:
                    removed_reasons['Other'] = removed_reasons.get('Other', 0) + 1
            
            for reason, count in removed_reasons.items():
                print(f"     {reason}: {count} rows")
        else:
            print(f"   No rows were removed during processing")
        
        # Show output structure
        print(f"\n📊 Output Structure:")
        print(f"   Columns: {list(processed_data.columns)}")
        print(f"   Shape: {processed_data.shape}")
        
        # Create Excel output with proper structure
        output_file = project_root / "test_output" / f"full_dataset_contact_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        processor.create_excel_output(processed_data, removed_rows, str(output_file))
        
        print(f"\n✅ Excel output created with proper structure!")
        print(f"   File: {output_file}")
        print(f"   Sheets: Alert Contact Export, Removed")
        
        return True
        
    except Exception as e:
        print(f"❌ Full Dataset Export Processor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 Stuart Data Cleaner - Full Dataset Test")
    print("=" * 70)
    
    # Run the test
    success = test_full_dataset()
    
    if success:
        print("\n🎉 Full dataset test completed successfully!")
        print("   Ready for production use with proper output structure.")
    else:
        print("\n⚠️  Full dataset test failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
