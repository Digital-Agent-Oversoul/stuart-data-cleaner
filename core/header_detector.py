#!/usr/bin/env python3
"""
Header Detection Module

Intelligent Excel header detection for different file types:
- Row 1 for test chunks
- Row 3 for production source files
"""

import pandas as pd
import logging
from typing import Tuple, List
from pathlib import Path

logger = logging.getLogger(__name__)

# Expected column names in production source files (in order)
EXPECTED_COLUMNS = [
    'Contract', 'Salesperson', 'Key', 'DEL', 'PU', 'Email', 'Contact Name',
    'Customer Name', 'Phone', 'Type', 'Business Type', 'Address 1', 'Address 2',
    'City', 'State', 'Zip', 'Delivery Date', 'Event Date', 'Return Date'
]

def detect_header_row(file_path: str, sheet_name: str = 'Sheet1', max_rows: int = 5) -> Tuple[int, pd.DataFrame]:
    """
    Detect the correct header row for Excel files by checking rows 1-5
    for expected column names.
    
    Args:
        file_path: Path to Excel file
        sheet_name: Name of sheet to check (default: 'Sheet1')
        max_rows: Maximum row to check for headers (default: 5)
        
    Returns:
        Tuple of (header_row_index, DataFrame with correct headers)
    """
    logger.info(f"Detecting header row for {file_path}")
    
    # Try different header rows
    for header_row in range(max_rows):
        try:
            logger.debug(f"Checking row {header_row + 1} for headers...")
            
            # Read Excel with this header row
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
            
            # Check if we have expected columns
            logger.debug(f"Row {header_row + 1}: Columns: {list(df.columns)}")
            has_expected = _has_expected_headers(df.columns)
            logger.debug(f"Row {header_row + 1}: Has expected headers: {has_expected}")
            
            if has_expected:
                logger.info(f"✅ Found expected headers on row {header_row + 1}")
                return header_row, df
            
            # Check if this row looks like data (not headers)
            looks_like_data = _looks_like_data_row(df.columns)
            logger.debug(f"Row {header_row + 1}: Looks like data: {looks_like_data}")
            
            if looks_like_data:
                logger.debug(f"Row {header_row + 1} appears to be data, not headers")
                continue
                
            logger.debug(f"Row {header_row + 1}: Found {len(df.columns)} columns")
            
        except Exception as e:
            logger.debug(f"Row {header_row + 1}: Error reading - {e}")
            continue
    
    # If no expected headers found, default to row 0 (first row)
    logger.warning("⚠️  No expected headers found in first 5 rows, using row 1 as default")
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
    return 0, df

def _has_expected_headers(columns: pd.Index) -> bool:
    """
    Check if columns match expected production file structure.
    
    Args:
        columns: DataFrame columns to check
        
    Returns:
        True if columns match expected structure
    """
    column_list = [str(col).strip() for col in columns]
    
    # Check for key expected columns
    key_columns = ['Email', 'Contact Name', 'Customer Name', 'Phone', 'City', 'State']
    found_key_columns = sum(1 for col in column_list if any(key in col for key in key_columns))
    
    # If we found several key columns, this is likely the right header row
    return found_key_columns >= 3

def _looks_like_data_row(columns: List[str]) -> bool:
    """
    Check if a row looks like data rather than headers.
    
    Args:
        columns: List of column values to check
        
    Returns:
        True if row appears to be data
    """
    # Check for patterns that indicate data rather than headers
    for col in columns:
        col_str = str(col).strip()
        
        # Check for email patterns
        if '@' in col_str and '.' in col_str:
            return True
            
        # Check for phone patterns
        if any(char.isdigit() for char in col_str) and len(col_str) >= 10:
            return True
            
        # Check for state abbreviations
        if len(col_str) == 2 and col_str.isalpha() and col_str.upper() in ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']:
            return True
            
        # Check for zip codes
        if col_str.isdigit() and len(col_str) == 5:
            return True
    
    return False

def load_data_with_header_detection(file_path: str, sheet_name: str = 'Sheet1') -> pd.DataFrame:
    """
    Load data with automatic header row detection.
    
    Args:
        file_path: Path to input file
        sheet_name: Name of sheet to load (default: 'Sheet1')
        
    Returns:
        DataFrame with correct headers
    """
    logger.info(f"Loading data with header detection: {file_path}")
    
    # Detect the correct header row
    header_row, df = detect_header_row(file_path, sheet_name)
    
    logger.info(f"Data loaded successfully:")
    logger.info(f"   Header row: {header_row + 1}")
    logger.info(f"   Columns: {len(df.columns)}")
    logger.info(f"   Rows: {len(df)}")
    logger.info(f"   Sample columns: {list(df.columns[:5])}")
    
    return df
