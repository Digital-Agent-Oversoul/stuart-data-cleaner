#!/usr/bin/env python3
"""
Export Processor

Production-ready Contact Export workflow processor that uses unified core logic
and provides Contact Export-specific output formatting.
"""

try:
    import pandas as pd
except ImportError as e:
    print("ERROR: pandas could not be imported. Please ensure it's installed:")
    print("   pip install pandas>=1.5.0")
    print(f"   Import error: {e}")
    raise

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment
except ImportError as e:
    print("ERROR: openpyxl could not be imported. Please ensure it's installed:")
    print("   pip install openpyxl>=3.0.0")
    print(f"   Import error: {e}")
    raise

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.data_processor import DataProcessor
from core.llm_engine import LLMEngine
from core.name_parser import NameParser

class ExportProcessor:
    """
    Contact Export workflow processor
    
    Uses unified core logic from DataProcessor and provides Contact Export-specific
    output formatting and error tracking.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        # Use the unified data processor for core logic
        self.data_processor = DataProcessor(config)
        # Keep direct access to LLM engine for workflow-specific needs
        self.llm_engine = LLMEngine(config.get('openai', {}))
        self.name_parser = NameParser(self.llm_engine)
        
    def process_contact_export(self, data: pd.DataFrame, original_source_data: pd.DataFrame = None, date_range: Optional[Dict[str, str]] = None) -> Tuple[pd.DataFrame, List[Dict]]:
        """
        Process contact export data using unified core logic
        
        Args:
            data: Raw contact export data with proper column mapping
            original_source_data: Original source data before mapping (for removed row tracking)
            date_range: Optional date range filter
            
        Returns:
            Tuple of (processed_data, removed_rows)
        """
        print("Processing Contact Export using unified core logic...")
        
        # Store original source data for removed row tracking
        if original_source_data is not None:
            self.original_columns = list(original_source_data.columns)
            source_data = original_source_data
        else:
            self.original_columns = list(data.columns)
            source_data = data
        
        # Track removed rows
        removed_rows = []
        
        # Use unified core logic for data processing
        processed_data = self.data_processor.process_contact_export_data(data)
        
        # Apply Contact Export-specific post-processing
        processed_data, export_removed_rows = self._apply_contact_export_specific_logic(processed_data, source_data)
        
        # Combine all removed rows
        removed_rows.extend(export_removed_rows)
        
        print(f"Contact Export processing complete using unified logic")
        print(f"   Records processed: {len(processed_data)}")
        print(f"   Records removed: {len(removed_rows)}")
        
        return processed_data, removed_rows
    
    def _apply_contact_export_specific_logic(self, data: pd.DataFrame, source_data: pd.DataFrame) -> Tuple[pd.DataFrame, List[Dict]]:
        """
        Apply Contact Export-specific logic after unified core processing
        
        Args:
            data: Data processed by unified core logic
            source_data: Original source data for removed row tracking
            
        Returns:
            Tuple of (processed_data, removed_rows)
        """
        removed_rows = []
        df_processed = data.copy()
        
        # 1. Remove rows with "Accounts Receivable" as Salesperson
        if 'Salesperson' in df_processed.columns:
            initial_count = len(df_processed)
            removed_accounts_df = df_processed[df_processed['Salesperson'].str.strip() == 'ACCOUNTS RECEIVABLE']
            
            # Track removed rows with original source data
            for idx, row in removed_accounts_df.iterrows():
                if idx in source_data.index:
                    original_row = source_data.loc[idx].to_dict()
                    removed_rows.append(original_row)
            
            df_processed = df_processed[df_processed['Salesperson'].str.strip() != 'ACCOUNTS RECEIVABLE']
            removed_accounts = initial_count - len(df_processed)
            if removed_accounts > 0:
                print(f"Removed {removed_accounts} rows with 'Accounts Receivable' as Salesperson")
        
        # 2. Apply Contact Export-specific data cleaning
        df_processed = self._clean_contact_export_data(df_processed)
        
        # 3. Remove rows without valid person names
        initial_count = len(df_processed)
        no_person_names_df = df_processed[
            ((df_processed['First name'].isna()) | (df_processed['First name'] == '') | (df_processed['First name'] == 'None')) & 
            ((df_processed['Last name'].isna()) | (df_processed['Last name'] == '') | (df_processed['Last name'] == 'None'))
        ]
        
        # Track removed rows
        for idx, row in no_person_names_df.iterrows():
            if idx in source_data.index:
                original_row = source_data.loc[idx].to_dict()
                removed_rows.append(original_row)
        
        df_processed = df_processed[
            ~(((df_processed['First name'].isna()) | (df_processed['First name'] == '') | (df_processed['First name'] == 'None')) & 
              ((df_processed['Last name'].isna()) | (df_processed['Last name'] == '') | (df_processed['Last name'] == 'None')))
        ]
        
        removed_no_names = initial_count - len(df_processed)
        if removed_no_names > 0:
            print(f"Removed {removed_no_names} rows without valid person names")
        
        # 4. Remove duplicate rows based on email
        initial_count = len(df_processed)
        df_processed['_temp_email_lower'] = df_processed['Email'].str.lower()
        df_processed = df_processed.drop_duplicates(subset=['_temp_email_lower'], keep='first')
        df_processed = df_processed.drop('_temp_email_lower', axis=1)
        
        removed_duplicates = initial_count - len(df_processed)
        if removed_duplicates > 0:
                            print(f"Removed {removed_duplicates} duplicate rows based on email")
        
        return df_processed, removed_rows
    
    def _clean_contact_export_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply Contact Export-specific data cleaning
        
        Args:
            data: Data to clean
            
        Returns:
            Cleaned data
        """
        df_cleaned = data.copy()
        
        # Clean phone numbers
        if 'Phone number' in df_cleaned.columns:
            df_cleaned['Phone number'] = df_cleaned['Phone number'].apply(self._clean_phone)
        
        # Clean state entries (remove leading/trailing spaces)
        if 'State' in df_cleaned.columns:
            df_cleaned['State'] = df_cleaned['State'].apply(lambda x: str(x).strip() if pd.notna(x) else x)
        
        # Clean business type entries
        if 'Business type' in df_cleaned.columns:
            df_cleaned['Business type'] = df_cleaned['Business type'].apply(lambda x: str(x).strip() if pd.notna(x) else x)
        
        return df_cleaned
    
    def _clean_phone(self, phone):
        """Clean phone numbers - return formatted string or None"""
        if pd.isna(phone) or phone == '' or phone == '0':
            return None
        
        phone_str = str(phone).strip()
        
        # If it's just "0", return None
        if phone_str == '0':
            return None
        
        # If all zeros, return None
        if phone_str == '0000000000':
            return None
        
        # Handle float values (from Excel conversion)
        if isinstance(phone, float):
            phone_str = str(int(phone))
        
        # Extract digits only
        import re
        digits = re.sub(r'\D', '', phone_str)
        
        # Format phone number
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            return None
    
    def create_excel_output(self, processed_data: pd.DataFrame, removed_rows: List[Dict], output_file: str):
        """
        Create Excel output with Contact Export-specific formatting
        
        Args:
            processed_data: Processed data to output
            removed_rows: Rows that were removed during processing
            output_file: Path to output file
        """
        
        wb = Workbook()
        
        # Create the main output sheet
        ws = wb.active
        ws.title = "Contact Export"
        
        # Add headers
        headers = [
            'Email', 'Business type', 'First name', 'Last name', 'Customer name',
            'Phone number', 'Sales person', 'Address 1', 'Address 2', 'City', 'State', 'Zip'
        ]
        
        for col_idx, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_idx, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')
        
        # Add data
        for row_idx, row_data in enumerate(processed_data.values, 2):
            for col_idx, value in enumerate(row_data, 1):
                ws.cell(row=row_idx, column=col_idx, value=value)
        
        # Create Removed sheet
        if removed_rows:
            ws_removed = wb.create_sheet("Removed")
            
            # Add headers using original column names
            for col_idx, col_name in enumerate(self.original_columns, 1):
                cell = ws_removed.cell(row=1, column=col_idx, value=col_name)
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center')
            
            # Add removed data
            for row_idx, row_data in enumerate(removed_rows, 2):
                for col_idx, col_name in enumerate(self.original_columns, 1):
                    value = row_data.get(col_name, '')
                    ws_removed.cell(row=row_idx, column=col_idx, value=value)
        
        # Save the workbook
        try:
            wb.save(output_file)
            print(f"✅ Excel output created: {output_file}")
            print(f"   Sheets: Contact Export ({len(processed_data)} rows), Removed ({len(removed_rows)} rows)")
        except Exception as e:
            raise RuntimeError(f"Failed to write output file {output_file}: {e}")
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics from unified processor"""
        return {
            'workflow_stats': {
                'workflow_type': 'contact_export',
                'processor_version': '1.0.0'
            },
            'core_stats': self.data_processor.get_processing_stats(),
            'llm_stats': self.llm_engine.get_stats() if hasattr(self.llm_engine, 'get_stats') else {}
        }
