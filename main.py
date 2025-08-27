#!/usr/bin/env python3
"""
Stuart Data Cleaning System - Main Entry Point

This module provides the main CLI interface and workflow orchestration
for the unified data cleaning system.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import pandas as pd
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.llm_engine import LLMEngine
from core.data_processor import DataProcessor
from workflows.broadly_survey.survey_processor import SurveyProcessor
from workflows.contact_export.export_processor import ExportProcessor
from config.config import Config


def setup_logging():
    """Setup basic logging for the application"""
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('data_cleaner.log')
        ]
    )
    return logging.getLogger(__name__)


def detect_header_row(file_path: str, max_header_row: int = 5) -> Tuple[int, pd.DataFrame]:
    """
    Detect the correct header row for Excel files by checking rows 1-5
    for expected column names.
    
    Args:
        file_path: Path to Excel file
        max_header_row: Maximum row to check for headers (default: 5)
        
    Returns:
        Tuple of (header_row_index, DataFrame with correct headers)
    """
    logger = setup_logging()
    
    # Expected column names that indicate we have the right headers
    expected_columns = [
        'Contact Name', 'Customer Name', 'Email', 'Email Address',
        'Location', 'Phone', 'Phone Number', 'Salesperson', 'Sales person',
        'Address 1', 'Address 2', 'City', 'State', 'Zip', 'Business type'
    ]
    
    # Try different header rows
    for header_row in range(max_header_row):
        try:
            logger.info(f"Checking row {header_row + 1} for headers...")
            
            # Read Excel with this header row
            df = pd.read_excel(file_path, header=header_row)
            
            # Check if we have expected columns
            found_columns = []
            for col in df.columns:
                if any(expected in str(col) for expected in expected_columns):
                    found_columns.append(col)
            
            # If we found several expected columns, this is likely the right header row
            if len(found_columns) >= 3:
                logger.info(f"✅ Found headers on row {header_row + 1}")
                logger.info(f"   Detected columns: {found_columns[:5]}...")
                return header_row, df
            
            logger.debug(f"Row {header_row + 1}: Found {len(found_columns)} expected columns")
            
        except Exception as e:
            logger.debug(f"Row {header_row + 1}: Error reading - {e}")
            continue
    
    # If no headers found, default to row 0 (first row)
    logger.warning("⚠️  No expected headers found in first 5 rows, using row 1 as default")
    df = pd.read_excel(file_path, header=0)
    return 0, df


def load_data_with_header_detection(file_path: str) -> Tuple[pd.DataFrame, int]:
    """
    Load data with automatic header row detection.
    
    Args:
        file_path: Path to input file
        
    Returns:
        Tuple of (DataFrame, header_row_index)
    """
    logger = setup_logging()
    
    if file_path.lower().endswith(('.xlsx', '.xls')):
        logger.info(f"Detecting headers in Excel file: {file_path}")
        header_row, df = detect_header_row(file_path)
        logger.info(f"Loaded {len(df)} records with headers from row {header_row + 1}")
        return df, header_row
    else:
        # CSV files - assume headers on first row
        logger.info(f"Loading CSV file: {file_path}")
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} records from CSV")
        return df, 0


def validate_input_file(file_path: str) -> bool:
    """Validate that input file exists and is readable"""
    if not os.path.exists(file_path):
        print(f"ERROR: Input file not found: {file_path}")
        return False
    
    if not file_path.lower().endswith(('.xlsx', '.xls', '.csv')):
        print(f"ERROR: Unsupported file format. Please use Excel (.xlsx, .xls) or CSV files.")
        return False
    
    return True


def process_survey_workflow(input_file: str, config: Config, output_dir: Optional[str] = None):
    """Process data using the Survey workflow with header detection"""
    logger = setup_logging()
    logger.info(f"Starting Survey workflow for: {input_file}")
    
    try:
        # Initialize processor with header detection
        processor = DataProcessor(config.__dict__)
        
        # Load data with header detection
        logger.info("Loading data with intelligent header detection...")
        data = processor.load_data(input_file)
        
        # Process data
        processed_data = processor.process_survey_data(data, location_filter=None)
        
        # Create output directory
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = os.path.join(os.path.dirname(input_file), "survey_output")
            os.makedirs(output_dir, exist_ok=True)
        
        # Generate location-segmented outputs
        locations = data['Location'].unique() if 'Location' in data.columns else ['unknown']
        for location in locations:
            location_data = processed_data[processed_data['Location'] == location] if 'Location' in processed_data.columns else processed_data
            output_file = os.path.join(output_dir, f"survey_{location.lower()}_{Path(input_file).stem}.xlsx")
            location_data.to_excel(output_file, index=False)
            logger.info(f"Survey data for {location} saved to: {output_file}")
        
        # Get processing statistics
        stats = processor.get_stats()
        logger.info(f"Survey processing complete: {stats['processed_records']} records processed")
        
        return True
        
    except Exception as e:
        logger.error(f"Survey workflow failed: {e}")
        return False


def process_contact_export_workflow(input_file: str, config: Config, output_dir: Optional[str] = None):
    """Process data using the Contact Export workflow with header detection"""
    logger = setup_logging()
    logger.info(f"Starting Contact Export workflow for: {input_file}")
    
    try:
        # Initialize processor with header detection
        processor = DataProcessor(config.__dict__)
        export_processor = ExportProcessor(config.__dict__)
        
        # Load data with header detection
        logger.info("Loading data with intelligent header detection...")
        data = processor.load_data(input_file)
        
        # Process data using "Removed as Remaining" approach
        processed_data, removed_rows = export_processor.process_contact_export(data, original_source_data=data)
        
        # Create output directory
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = os.path.join(os.path.dirname(input_file), "contact_export_output")
            os.makedirs(output_dir, exist_ok=True)
        
        # Generate aggregated output with removed items sheet
        output_file = os.path.join(output_dir, f"contact_export_{Path(input_file).stem}.xlsx")
        
        # Create Excel output with multiple sheets
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Main Contact Export sheet
            processed_data.to_excel(writer, sheet_name='Contact Export', index=False)
            
            # Removed items sheet with reasons
            if len(removed_rows) > 0:
                removed_rows.to_excel(writer, sheet_name='Removed', index=False)
            else:
                # Create empty removed sheet with headers
                empty_removed = pd.DataFrame(columns=['Removal Reason'] + list(data.columns))
                empty_removed.to_excel(writer, sheet_name='Removed', index=False)
        
        logger.info(f"Contact Export data saved to: {output_file}")
        
        # Create summary report
        summary_file = os.path.join(output_dir, f"contact_export_summary_{Path(input_file).stem}.txt")
        with open(summary_file, 'w') as f:
            f.write(f"Contact Export Processing Summary\n")
            f.write(f"================================\n")
            f.write(f"Input file: {input_file}\n")
            f.write(f"Processing date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total records processed: {len(processed_data)}\n")
            f.write(f"Records removed: {len(removed_rows)}\n")
            f.write(f"Date range: All dates\n")
        
        logger.info(f"Summary report saved to: {summary_file}")
        
        return True
        
    except Exception as e:
        logger.error(f"Contact Export workflow failed: {e}")
        return False


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Stuart Data Cleaning System - Unified Data Processing Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process survey data with progress reporting
  python main.py survey data.xlsx --progress
  
  # Process contact export without progress reporting
  python main.py contact data.xlsx --no-progress
  
  # Process with custom configuration
  python main.py survey data.xlsx --config custom_config.json
        """
    )
    
    parser.add_argument(
        'process_type',
        choices=['survey', 'contact'],
        help='Type of processing: survey (location-segmented) or contact (aggregated)'
    )
    
    parser.add_argument(
        'input_file',
        help='Path to input Excel file'
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Path to configuration file (optional)'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        help='Output directory (overrides config)'
    )
    
    parser.add_argument(
        '--progress', '--show-progress',
        action='store_true',
        default=True,
        help='Show progress reporting (default: enabled)'
    )
    
    parser.add_argument(
        '--no-progress', '--hide-progress',
        action='store_true',
        help='Hide progress reporting'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Handle progress reporting flags
    if args.no_progress:
        show_progress = False
    else:
        show_progress = args.progress
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logging()
    logger.setLevel(log_level)
    
    # Load configuration
    try:
        config = Config(args.config)
        
        # Override progress setting from CLI
        config.processing.show_progress = show_progress
        
        logger.info(f"Configuration loaded successfully")
        logger.info(f"Progress reporting: {'enabled' if show_progress else 'disabled'}")
        logger.info(f"Retry settings: {config.processing.max_retries} attempts, {config.processing.retry_delay_ms}ms delay")
        
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)
    
    # Validate input file
    if not os.path.exists(args.input_file):
        logger.error(f"Input file not found: {args.input_file}")
        sys.exit(1)
    
    # Process based on type
    try:
        if args.process_type == 'survey':
            process_survey_workflow(args.input_file, config, args.output_dir)
        elif args.process_type == 'contact':
            process_contact_export_workflow(args.input_file, config, args.output_dir)
        else:
            logger.error(f"Unknown process type: {args.process_type}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
