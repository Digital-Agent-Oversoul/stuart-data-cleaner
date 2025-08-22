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
from typing import Dict, Any, Optional
import pandas as pd

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


def validate_input_file(file_path: str) -> bool:
    """Validate that input file exists and is readable"""
    if not os.path.exists(file_path):
        print(f"ERROR: Input file not found: {file_path}")
        return False
    
    if not file_path.lower().endswith(('.xlsx', '.xls', '.csv')):
        print(f"ERROR: Unsupported file format. Please use Excel (.xlsx, .xls) or CSV files.")
        return False
    
    return True


def process_survey_workflow(config: Config, input_file: str, output_dir: str, location_filter: Optional[str] = None):
    """Process data using the Survey workflow"""
    logger = setup_logging()
    logger.info(f"Starting Survey workflow processing: {input_file}")
    
    try:
        # Initialize survey processor
        processor = SurveyProcessor(config.__dict__)
        
        # Load and process data
        data = pd.read_excel(input_file) if input_file.endswith(('.xlsx', '.xls')) else pd.read_csv(input_file)
        
        logger.info(f"Loaded {len(data)} records for processing")
        
        # Process data
        processed_data = processor.process_survey_data(data, location_filter)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate location-segmented outputs
        if location_filter:
            # Single location output
            output_file = os.path.join(output_dir, f"survey_{location_filter.lower()}_{Path(input_file).stem}.xlsx")
            processed_data.to_excel(output_file, index=False)
            logger.info(f"Survey data saved to: {output_file}")
        else:
            # Multiple location outputs
            locations = data['location'].unique() if 'location' in data.columns else ['unknown']
            for location in locations:
                location_data = processed_data[processed_data['location'] == location] if 'location' in processed_data.columns else processed_data
                output_file = os.path.join(output_dir, f"survey_{location.lower()}_{Path(input_file).stem}.xlsx")
                location_data.to_excel(output_file, index=False)
                logger.info(f"Survey data for {location} saved to: {output_file}")
        
        # Get processing statistics
        stats = processor.get_processing_stats()
        logger.info(f"Processing completed. LLM calls: {stats.get('llm_stats', {}).get('total_calls', 0)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in Survey workflow: {str(e)}")
        print(f"ERROR: Error processing survey data: {str(e)}")
        return False


def process_contact_export_workflow(config: Config, input_file: str, output_dir: str, date_range: Optional[Dict[str, str]] = None):
    """Process data using the Contact Export workflow"""
    logger = setup_logging()
    logger.info(f"Starting Contact Export workflow processing: {input_file}")
    
    try:
        # Initialize export processor
        processor = ExportProcessor(config.__dict__)
        
        # Load and process data
        data = pd.read_excel(input_file) if input_file.endswith(('.xlsx', '.xls')) else pd.read_csv(input_file)
        
        logger.info(f"Loaded {len(data)} records for processing")
        
        # Process data
        processed_data = processor.process_contact_export(data, date_range)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate aggregated output
        output_file = os.path.join(output_dir, f"contact_export_{Path(input_file).stem}.xlsx")
        processed_data.to_excel(output_file, index=False)
        logger.info(f"Contact export data saved to: {output_file}")
        
        # Generate summary report
        summary_file = os.path.join(output_dir, f"contact_export_summary_{Path(input_file).stem}.txt")
        with open(summary_file, 'w') as f:
            f.write(f"Contact Export Processing Summary\n")
            f.write(f"Generated: {pd.Timestamp.now()}\n")
            f.write(f"Input file: {input_file}\n")
            f.write(f"Total records processed: {len(processed_data)}\n")
            f.write(f"Date range: {date_range or 'All dates'}\n")
        
        logger.info(f"Summary report saved to: {summary_file}")
        
        # Get processing statistics
        stats = processor.get_processing_stats()
        logger.info(f"Processing completed. LLM calls: {stats.get('llm_stats', {}).get('total_calls', 0)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in Contact Export workflow: {str(e)}")
        print(f"ERROR: Error processing contact export data: {str(e)}")
        return False


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Stuart Data Cleaning System - Unified data processing engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py survey data.xlsx                    # Process survey data
  python main.py survey data.xlsx --location Dublin # Process survey data for Dublin location
  python main.py contact data.xlsx                   # Process contact export data
  python main.py contact data.xlsx --start 2024-01-01 --end 2024-12-31  # Process with date range
        """
    )
    
    # Main workflow selection
    parser.add_argument(
        'workflow',
        choices=['survey', 'contact'],
        help='Workflow to execute: survey (Broadly Survey) or contact (Contact Export)'
    )
    
    # Input file
    parser.add_argument(
        'input_file',
        help='Path to input Excel or CSV file'
    )
    
    # Output options
    parser.add_argument(
        '--output-dir', '-o',
        default='output',
        help='Output directory for processed files (default: output)'
    )
    
    # Survey-specific options
    parser.add_argument(
        '--location', '-l',
        help='Location filter for survey processing (e.g., Dublin, Milpitas)'
    )
    
    # Contact export-specific options
    parser.add_argument(
        '--start',
        help='Start date for contact export (YYYY-MM-DD format)'
    )
    parser.add_argument(
        '--end',
        help='End date for contact export (YYYY-MM-DD format)'
    )
    
    # Configuration options
    parser.add_argument(
        '--config', '-c',
        help='Path to configuration file'
    )
    
    # Verbose logging
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not validate_input_file(args.input_file):
        sys.exit(1)
    
    # Setup configuration
    try:
        config = Config(args.config)
        if args.verbose:
            config.processing.enable_progress_tracking = True
    except Exception as e:
        print(f"ERROR: Error loading configuration: {str(e)}")
        sys.exit(1)
    
    # Setup logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Process based on workflow
    success = False
    
    if args.workflow == 'survey':
        success = process_survey_workflow(config, args.input_file, args.output_dir, args.location)
    elif args.workflow == 'contact':
        date_range = None
        if args.start or args.end:
            date_range = {}
            if args.start:
                date_range['start'] = args.start
            if args.end:
                date_range['end'] = args.end
        success = process_contact_export_workflow(config, args.input_file, args.output_dir, date_range)
    
    if success:
        print(f"✅ {args.workflow.title()} workflow completed successfully!")
        print(f"📁 Output files saved to: {os.path.abspath(args.output_dir)}")
    else:
        print(f"ERROR: {args.workflow.title()} workflow failed. Check logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
