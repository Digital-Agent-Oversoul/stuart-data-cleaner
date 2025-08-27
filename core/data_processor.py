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
from .header_detector import load_data_with_header_detection

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
        
        # Transform config structure to match LLM engine expectations
        llm_config = {
            'openai': {
                'api_key': self._get_config_value('openai_api_key') or self._get_config_value('llm.openai_api_key'),
                'model': self._get_config_value('openai_model', 'gpt-4o-mini') or self._get_config_value('llm.openai_model', 'gpt-4o-mini'),
                'max_tokens': self._get_config_value('max_tokens', 150) or self._get_config_value('llm.max_tokens', 150),
                'temperature': self._get_config_value('temperature', 0.1) or self._get_config_value('llm.temperature', 0.1)
            },
            'ollama': {
                'base_url': self._get_config_value('ollama_base_url', 'http://localhost:11434') or self._get_config_value('llm.ollama_base_url', 'http://localhost:11434'),
                'model': self._get_config_value('ollama_model', 'qwen2.5:7b-instruct-q4_K_M') or self._get_config_value('llm.ollama_model', 'qwen2.5:7b-instruct-q4_K_M')
            },
            'max_retries': self._get_config_value('max_retries', 3) or self._get_config_value('processing.max_retries', 3),
            'retry_delay_ms': self._get_config_value('retry_delay_ms', 1000) or self._get_config_value('processing.retry_delay_ms', 1000),
            'show_progress': self._get_config_value('show_progress', True) or self._get_config_value('processing.show_progress', True)
        }
        self.llm_engine = LLMEngine(llm_config)
        self.name_parser = NameParser(self.llm_engine)
        
        # Processing statistics
        self.stats = {
            'total_records': 0,
            'processed_records': 0,
            'failed_records': 0,
            'start_time': datetime.now(),
            'end_time': None
        }
        
        # Performance optimization: lazy evaluation for removed rows
        self._removed_rows_cache = None
        self._retry_failure_indices = []
    
    def _get_config_value(self, key_path, default=None):
        """Get config value from nested path, handling both dict and object access"""
        if isinstance(self.config, dict):
            # Handle dictionary access
            if '.' in key_path:
                parts = key_path.split('.')
                current = self.config
                for part in parts:
                    if isinstance(current, dict) and part in current:
                        current = current[part]
                    else:
                        return default
                return current
            else:
                return self.config.get(key_path, default)
        else:
            # Handle object access
            if '.' in key_path:
                parts = key_path.split('.')
                current = self.config
                for part in parts:
                    if hasattr(current, part):
                        current = getattr(current, part)
                    else:
                        return default
                return current
            else:
                return getattr(self.config, key_path, default)
    
    def load_data(self, file_path: str, sheet_name: str = 'Sheet1') -> pd.DataFrame:
        """
        Load data with intelligent header detection.
        
        Args:
            file_path: Path to input file
            sheet_name: Name of sheet to load
            
        Returns:
            DataFrame with correct headers
        """
        logger.info(f"Loading data with header detection: {file_path}")
        return load_data_with_header_detection(file_path, sheet_name)
    
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
        cleaned_data = self._clean_names_with_progress(cleaned_data)
        
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
        """
        Remove records marked for removal with performance optimization.
        
        Args:
            data: DataFrame with records to process
            
        Returns:
            DataFrame with invalid records removed
        """
        # Use vectorized operation for better performance
        valid_mask = data['_mark_for_removal'] == False
        valid_data = data[valid_mask].copy()
        
        removed_count = len(data) - len(valid_data)
        logger.info(f"Removed {removed_count} invalid records")
        
        # Clean up processing columns
        if '_mark_for_removal' in valid_data.columns:
            valid_data = valid_data.drop(columns=['_mark_for_removal'])
        
        return valid_data
    
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

    def get_retry_failure_indices(self) -> List[int]:
        """
        Get indices of records that failed after retry attempts.
        
        Returns:
            List of row indices that failed processing
        """
        return self._retry_failure_indices.copy()
    
    def _clean_names_with_progress(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean names with progress reporting and retry logic.
        
        Args:
            data: DataFrame with name data to clean
            
        Returns:
            DataFrame with cleaned names and processing metadata
        """
        logger.info(f"Cleaning names for {len(data)} records...")
        
        # Add processing columns
        data = data.copy()
        data['_mark_for_removal'] = False
        data['_processing_method'] = ''
        data['_confidence_score'] = 0.0
        data['_error_message'] = ''
        
        for idx, row in data.iterrows():
            try:
                # Extract name fields
                contact_name = str(row.get('contact_name', '')).strip()
                customer_name = str(row.get('customer_name', '')).strip()
                email = str(row.get('email', '')).strip()
                
                # Handle pandas NaN values properly
                if contact_name == 'nan' or pd.isna(row.get('contact_name')):
                    contact_name = ''
                if customer_name == 'nan' or pd.isna(row.get('customer_name')):
                    customer_name = ''
                if email == 'nan' or pd.isna(row.get('email')):
                    email = ''
                
                if self._get_config_value('show_progress', True) or self._get_config_value('processing.show_progress', True):
                    print(f"🔄 Processing row {idx + 1}: {contact_name} | {customer_name} | {email}")
                
                # Parse name using LLM engine
                result = self.llm_engine.parse_name(contact_name, customer_name, email)
                
                if result.success:
                    # Update row with parsed results
                    data.at[idx, 'first_name'] = result.first_name
                    data.at[idx, 'last_name'] = result.last_name
                    data.at[idx, '_processing_method'] = result.processing_method
                    data.at[idx, '_confidence_score'] = result.confidence
                    
                    if self._get_config_value('show_progress', True) or self._get_config_value('processing.show_progress', True):
                        print(f"   ✅ Cleaned: {result.first_name} {result.last_name} (method: {result.processing_method}, confidence: {result.confidence:.2f})")
                else:
                    # Mark for removal if processing failed
                    data.at[idx, '_mark_for_removal'] = True
                    data.at[idx, '_error_message'] = result.error_message
                    
                    if self._get_config_value('show_progress', True) or self._get_config_value('processing.show_progress', True):
                        print(f"   ❌ Failed: {result.error_message}")
                    
                    # Track retry failures
                    self._retry_failure_indices.append(idx)
                    
            except Exception as e:
                logger.error(f"Error processing row {idx}: {e}")
                data.at[idx, '_mark_for_removal'] = True
                data.at[idx, '_error_message'] = str(e)
                self._retry_failure_indices.append(idx)
        
        return data
