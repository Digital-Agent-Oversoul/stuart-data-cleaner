#!/usr/bin/env python3
"""
Test script for ExportProcessor with header detection and "Removed as Remaining" approach
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
from workflows.contact_export.export_processor import ExportProcessor

def test_export_processor():
    """Test the export processor with header detection"""
    print("🧪 Testing ExportProcessor with header detection...")
    
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
    
    # Initialize processors
    try:
        data_processor = DataProcessor(config)
        export_processor = ExportProcessor(config)
        print("✅ Processors initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize processors: {e}")
        return False
    
    # Find test dataset
    test_datasets_dir = project_root / "tests" / "test_datasets"
    if not test_datasets_dir.exists():
        print(f"❌ Test datasets directory not found: {test_datasets_dir}")
        return False
    
    # Get list of test datasets
    test_files = list(test_datasets_dir.glob("*.xlsx"))
    if not test_files:
        print(f"❌ No test datasets found in {test_datasets_dir}")
        return False
    
    # Use a test dataset with the correct columns (Contact Name, Customer Name, Email)
    test_dataset = "test_chunk_01_20250821_172404.xlsx"
    print(f"�� Using test dataset: {test_dataset}")
    
    # Load data with header detection
    try:
        print("🔄 Loading data with header detection...")
        data = data_processor.load_data(str(test_datasets_dir / test_dataset))
        print(f"✅ Data loaded: {len(data)} rows, {len(data.columns)} columns")
        print(f"   Sample columns: {list(data.columns[:5])}")
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return False
    
    # Process contact export
    try:
        print("🔄 Processing contact export...")
        processed_data, removed_rows = export_processor.process_contact_export(
            data, original_source_data=data
        )
        print(f"✅ Processing complete:")
        print(f"   Processed records: {len(processed_data)}")
        print(f"   Removed records: {len(removed_rows)}")
    except Exception as e:
        print(f"❌ Failed to process contact export: {e}")
        return False
    
    # Create test output
    test_output_dir = project_root / "tests" / "test_outputs"
    test_output_dir.mkdir(exist_ok=True)
    
    output_file = test_output_dir / f"test_export_{test_dataset.replace('.xlsx', '')}.xlsx"
    
    try:
        # Use the export processor's create_excel_output method for proper formatting
        export_processor.create_excel_output(processed_data, removed_rows, str(output_file))
        
        print(f"✅ Test output saved to: {output_file}")
        
        # Verify output structure
        if len(processed_data) > 0:
            print(f"   ✅ Processed data has {len(processed_data)} rows")
            if 'first_name' in processed_data.columns and 'last_name' in processed_data.columns:
                print(f"   ✅ Name columns present: first_name, last_name")
            else:
                print(f"   ⚠️  Name columns missing: {list(processed_data.columns)}")
        
        if len(removed_rows) > 0:
            print(f"   ✅ Removed data has {len(removed_rows)} rows")
            if 'Removal Reason' in removed_rows.columns:
                print(f"   ✅ Removal reasons present")
                # Show sample removal reasons
                reasons = removed_rows['Removal Reason'].value_counts()
                print(f"   📊 Removal reason distribution:")
                for reason, count in reasons.head(5).items():
                    print(f"      {reason}: {count}")
            else:
                print(f"   ⚠️  Removal reasons missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create test output: {e}")
        return False

if __name__ == "__main__":
    success = test_export_processor()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")
        sys.exit(1)
