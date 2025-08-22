"""
Unified Data Processor Module

This module consolidates the data cleaning logic from both Contact Export and 
Broadly Survey scripts into a unified processing engine that both processes can use.
"""

import pandas as pd
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from .llm_engine import LLMEngine, LLMResponse
from .name_parser import NameParser

logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Unified data processor that handles both Survey and Contact Export operations
    with shared cleaning logic and independent output handling.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the data processor with configuration
        
        Args:
            config: Configuration dictionary containing LLM and processing settings
        """
        self.config = config
        self.llm_engine = LLMEngine(config)
        self.name_parser = NameParser(self.llm_engine)
        
        # Processing statistics
        self.stats = {
            'total_records': 0,
            'processed_records': 0,
            'failed_records': 0,
            'start_time': datetime.now(),
            'end_time': None
        }
        
    def process_survey_data(self, data: pd.DataFrame, location_filter: Optional[str] = None) -> pd.DataFrame:
        """
        Process data for Broadly Survey output (location-segmented, smaller files)
        
        Args:
            data: Raw data DataFrame
            location_filter: Optional location filter (e.g., 'Dublin', 'Milpitas')
            
        Returns:
            Processed DataFrame ready for survey output
        """
        logger.info(f"Processing survey data: {len(data)} records")
        
        # Apply location filter if specified
        if location_filter:
            data = data[data['Location'] == location_filter].copy()
            logger.info(f"Filtered to {location_filter}: {len(data)} records")
        
        # Process the data using unified cleaning logic
        processed_data = self._apply_unified_cleaning(data)
        
        # Apply survey-specific transformations
        processed_data = self._apply_survey_transformations(processed_data)
        
        # Update statistics
        self.stats['total_records'] += len(data)
        self.stats['processed_records'] += len(processed_data)
        
        logger.info(f"Survey data processing complete: {len(processed_data)} records")
        return processed_data
    
    def process_contact_export_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Process data for Contact Export output (aggregated, larger files)
        
        Args:
            data: Raw data DataFrame
            
        Returns:
            Processed DataFrame ready for contact export
        """
        logger.info(f"Processing contact export data: {len(data)} records")
        
        # Process the data using unified cleaning logic
        processed_data = self._apply_unified_cleaning(data)
        
        # Apply contact export-specific transformations
        processed_data = self._apply_contact_export_transformations(processed_data)
        
        # Update statistics
        self.stats['total_records'] += len(data)
        self.stats['processed_records'] += len(processed_data)
        
        logger.info(f"Contact export processing complete: {len(processed_data)} records")
        return processed_data
    
    def _apply_unified_cleaning(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply unified data cleaning logic that both processes share
        
        Args:
            data: Raw data DataFrame
            
        Returns:
            Cleaned DataFrame with unified logic applied
        """
        logger.info("Applying unified cleaning logic")
        
        # Create a copy to avoid modifying original data
        cleaned_data = data.copy()
        
        # Standardize column names
        cleaned_data = self._standardize_columns(cleaned_data)
        
        # Clean and parse names using the unified LLM engine
        cleaned_data = self._clean_names(cleaned_data)
        
        # Clean email addresses
        cleaned_data = self._clean_emails(cleaned_data)
        
        # Remove duplicates and invalid records
        cleaned_data = self._remove_invalid_records(cleaned_data)
        
        # Sort by relevant columns
        cleaned_data = cleaned_data.sort_values(['last_name', 'first_name', 'email'])
        
        return cleaned_data
    
    def _standardize_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names and structure"""
        # Map common column variations to standard names
        column_mapping = {
            'Contact Name': 'contact_name',
            'Customer Name': 'customer_name',
            'Email': 'email',
            'Email Address': 'email',
            'Location': 'location',
            'Phone': 'phone',
            'Phone Number': 'phone'
        }
        
        # Rename columns if they exist
        for old_name, new_name in column_mapping.items():
            if old_name in data.columns:
                data = data.rename(columns={old_name: new_name})
        
        # Ensure required columns exist
        required_columns = ['contact_name', 'customer_name', 'email']
        for col in required_columns:
            if col not in data.columns:
                data[col] = None
                logger.warning(f"Missing required column: {col}, added as null")
        
        return data
    
    def _clean_names(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and parse names using the unified LLM engine
        
        Args:
            data: DataFrame with contact_name, customer_name, email columns
            
        Returns:
            DataFrame with cleaned first_name and last_name columns
        """
        logger.info("Cleaning and parsing names using unified LLM engine")
        
        # Initialize new columns
        data['first_name'] = None
        data['last_name'] = None
        data['name_confidence'] = 0.0
        data['processing_method'] = None
        
        # Process names in batches for efficiency
        batch_size = 50
        total_records = len(data)
        
        for i in range(0, total_records, batch_size):
            batch_end = min(i + batch_size, total_records)
            batch_data = data.iloc[i:batch_end]
            
            logger.info(f"Processing name batch {i//batch_size + 1}: records {i+1}-{batch_end}")
            
            for idx, row in batch_data.iterrows():
                try:
                    # Parse name using unified LLM engine
                    result = self.name_parser.parse_name(
                        contact_name=row.get('contact_name'),
                        customer_name=row.get('customer_name'),
                        email=row.get('email')
                    )
                    
                    if result.success:
                        data.at[idx, 'first_name'] = result.first_name
                        data.at[idx, 'last_name'] = result.last_name
                        data.at[idx, 'name_confidence'] = result.confidence
                        data.at[idx, 'processing_method'] = result.processing_method
                    else:
                        logger.warning(f"Name parsing failed for record {idx}: {result.error_message}")
                        data.at[idx, 'name_confidence'] = 0.0
                        data.at[idx, 'processing_method'] = 'failed'
                        
                except Exception as e:
                    logger.error(f"Error processing name for record {idx}: {e}")
                    data.at[idx, 'name_confidence'] = 0.0
                    data.at[idx, 'processing_method'] = 'error'
        
        return data
    
    def _clean_emails(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize email addresses"""
        logger.info("Cleaning email addresses")
        
        if 'email' not in data.columns:
            return data
        
        # Clean email addresses
        data['email'] = data['email'].astype(str).str.strip()
        
        # Handle multiple emails (take first personal-looking email)
        data['email'] = data['email'].apply(self._extract_primary_email)
        
        # Remove invalid email patterns
        data['email'] = data['email'].apply(self._validate_email)
        
        return data
    
    def _extract_primary_email(self, email_str: str) -> Optional[str]:
        """Extract the primary email from a string that may contain multiple emails"""
        if pd.isna(email_str) or email_str == '':
            return None
        
        # Split by common separators
        emails = email_str.replace(';', ',').replace('|', ',').split(',')
        emails = [e.strip() for e in emails if e.strip()]
        
        if not emails:
            return None
        
        # Prefer personal-looking emails over business emails
        for email in emails:
            if self._is_personal_email(email):
                return email
        
        # If no personal emails found, return the first valid email
        return emails[0] if emails else None
    
    def _is_personal_email(self, email: str) -> bool:
        """Check if an email looks like a personal email rather than business"""
        if not email or '@' not in email:
            return False
        
        # Business email patterns to avoid
        business_patterns = [
            'info@', 'sales@', 'support@', 'admin@', 'noreply@',
            'workplace-support@', 'help@', 'contact@', 'service@'
        ]
        
        email_lower = email.lower()
        for pattern in business_patterns:
            if email_lower.startswith(pattern):
                return False
        
        # Personal email patterns to prefer
        personal_patterns = [
            'firstname.lastname@', 'firstinitiallastname@',
            'firstname@', 'lastname@'
        ]
        
        for pattern in personal_patterns:
            if pattern in email_lower:
                return True
        
        return True  # Default to personal if no clear business indicators
    
    def _validate_email(self, email: str) -> Optional[str]:
        """Basic email validation"""
        if pd.isna(email) or email == '':
            return None
        
        # Basic email format validation
        if '@' in email and '.' in email.split('@')[1]:
            return email
        
        return None
    
    def _remove_invalid_records(self, data: pd.DataFrame) -> pd.DataFrame:
        """Remove records that don't meet quality standards"""
        logger.info("Removing invalid records")
        
        initial_count = len(data)
        
        # Remove records with no valid names
        data = data[
            (data['first_name'].notna()) & 
            (data['first_name'] != '') &
            (data['name_confidence'] > 0.3)  # Minimum confidence threshold
        ]
        
        # Remove records with no valid email
        data = data[data['email'].notna()]
        
        # Remove completely empty rows
        data = data.dropna(how='all')
        
        final_count = len(data)
        removed_count = initial_count - final_count
        
        logger.info(f"Removed {removed_count} invalid records: {initial_count} -> {final_count}")
        
        return data
    
    def _apply_survey_transformations(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply survey-specific transformations"""
        logger.info("Applying survey-specific transformations")
        
        # Add survey-specific columns
        data['survey_ready'] = True
        data['location_segment'] = data.get('location', 'Unknown')
        
        # Ensure required survey columns exist
        required_survey_columns = ['first_name', 'last_name', 'email', 'location']
        for col in required_survey_columns:
            if col not in data.columns:
                data[col] = None
        
        return data
    
    def _apply_contact_export_transformations(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply contact export-specific transformations"""
        logger.info("Applying contact export-specific transformations")
        
        # Add contact export-specific columns
        data['export_ready'] = True
        data['export_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Ensure required export columns exist
        required_export_columns = ['first_name', 'last_name', 'email', 'phone']
        for col in required_export_columns:
            if col not in data.columns:
                data[col] = None
        
        return data
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get comprehensive processing statistics"""
        self.stats['end_time'] = datetime.now()
        
        # Get LLM engine stats
        llm_stats = self.llm_engine.get_stats()
        
        # Combine stats
        combined_stats = {
            **self.stats,
            'llm_stats': {
                'total_llm_calls': llm_stats.total_records,
                'openai_processed': llm_stats.llm_processed,
                'ollama_fallback': llm_stats.ollama_fallback,
                'rule_based_fallback': llm_stats.rule_based_fallback,
                'llm_errors': llm_stats.errors
            },
            'success_rate': (self.stats['processed_records'] / self.stats['total_records']) if self.stats['total_records'] > 0 else 0,
            'processing_duration': (self.stats['end_time'] - self.stats['start_time']).total_seconds() if self.stats['end_time'] else 0
        }
        
        return combined_stats
    
    def reset_stats(self):
        """Reset processing statistics"""
        self.stats = {
            'total_records': 0,
            'processed_records': 0,
            'failed_records': 0,
            'start_time': datetime.now(),
            'end_time': None
        }
        self.llm_engine.reset_stats()
