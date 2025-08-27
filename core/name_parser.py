"""
Name Parser Module

This module provides a clean interface for name parsing operations,
integrating with the unified LLM engine.
"""

import re
import logging
from typing import Optional, Tuple, Dict, Any
from .llm_engine import LLMEngine, LLMResponse

logger = logging.getLogger(__name__)

class NameParser:
    """Unified name parser with LLM integration and fallback systems"""
    
    def __init__(self, llm_engine: LLMEngine):
        self.llm_engine = llm_engine
        
    def parse_name(self, contact_name: str, customer_name: str, email: str) -> LLMResponse:
        """
        Parse name from contact information using the unified LLM engine
        
        Args:
            contact_name: Contact name field from the data
            customer_name: Customer name field from the data
            email: Email address field from the data
            
        Returns:
            LLMResponse with parsed name information and confidence scores
        """
        # Clean and validate input data
        contact_name = self._clean_input(contact_name)
        customer_name = self._clean_input(customer_name)
        email = self._clean_input(email)
        
        # Use the unified LLM engine for parsing
        result = self.llm_engine.parse_name(contact_name, customer_name, email)
        
        # Post-process the result if successful
        if result.success and result.first_name:
            result.first_name = self._clean_name_for_display(result.first_name)
        if result.success and result.last_name:
            result.last_name = self._clean_name_for_display(result.last_name)
            # Validate last name
            if not self._is_valid_last_name(result.last_name):
                result.last_name = None
                result.confidence *= 0.8  # Reduce confidence if last name is invalid
        
        return result
    
    def _clean_input(self, value: Any) -> Optional[str]:
        """Clean and validate input values"""
        if value is None:
            return None
        
        value_str = str(value).strip()
        
        # Check for common null/empty values
        if value_str.lower() in ['', 'nan', 'none', 'null', 'fff']:
            return None
            
        return value_str
    
    def _clean_name_for_display(self, name: str) -> str:
        """Clean name for display, handling special characters and formatting"""
        if not name or name.lower() in ['null', 'none']:
            return None
        
        name_str = str(name).strip()
        
        # Handle hyphenated names with spaces around hyphens
        # "EWING - ERVIN" becomes "Ewing-Ervin"
        name_str = re.sub(r'\s*-\s*', '-', name_str)
        
        # Remove numbers from names (but keep hyphens and other separators)
        name_str = re.sub(r'\d+', '', name_str)
        
        # Remove extra spaces but preserve hyphens
        name_str = ' '.join(name_str.split())
        name_str = name_str.title()
        
        return name_str
    
    def _is_valid_last_name(self, last_name: str) -> bool:
        """Validate if a last name is reasonable"""
        if not last_name or len(last_name) < 2:
            return False
        
        # Check for common business terms that shouldn't be last names
        business_indicators = [
            'llc', 'inc', 'corp', 'group', 'center', 'catering', 'entertainment',
            'restaurant', 'bhavan', 'school', 'church', 'university', 'college',
            'hospital', 'clinic', 'foundation', 'association', 'organization',
            'institute', 'system', 'network', 'partners', 'alliance', 'productions',
            'steakhouse', 'wine bar', 'innovation', 'technology', 'real estate',
            'booster club', 'tradition', 'residence', 'district', 'county',
            'office', 'department', 'division', 'bureau', 'agency', 'authority',
            'commission', 'board', 'council', 'committee', 'team', 'staff',
            'personnel', 'employees', 'workers', 'members', 'volunteers',
            'capital', 'modern', 'senior', 'living', 'elementary', 'solutions',
            'systems', 'innovations', 'research', 'corporation', 'print',
            'design', 'decor', 'tile', 'kitchen', 'creations', 'streamline',
            'expectations', 'succulent', 'cactus', 'climate', 'week', 'zoo',
            'hotel', 'cafe', 'deli', 'plaza', 'gymnastics', 'government',
            'city', 'arena', 'americas', 'southern', 'cloud', 'west', 'pacific',
            'luxe', 'real-time'
        ]
        
        last_name_lower = last_name.lower()
        if last_name_lower in business_indicators:
            return False
        
        # Check for suspicious patterns
        if len(last_name) > 50:  # Unreasonably long
            return False
        
        if re.match(r'^[A-Z\s]+$', last_name) and len(last_name) > 20:  # All caps and very long
            return False
        
        return True
    
    def batch_parse_names(self, data: list) -> list:
        """
        Parse names in batch for efficiency
        
        Args:
            data: List of dictionaries with 'contact_name', 'customer_name', 'email' keys
            
        Returns:
            List of LLMResponse objects
        """
        results = []
        
        for item in data:
            contact_name = item.get('contact_name')
            customer_name = item.get('customer_name')
            email = item.get('email')
            
            result = self.parse_name(contact_name, customer_name, email)
            results.append(result)
            
            # Log progress for large batches
            if len(results) % 100 == 0:
                logger.info(f"Processed {len(results)} names...")
        
        return results
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get statistics about the processing operations"""
        stats = self.llm_engine.get_stats()
        return {
            'total_records': stats.total_records,
            'llm_processed': stats.llm_processed,
            'ollama_fallback': stats.ollama_fallback,
            'rule_based_fallback': stats.rule_based_fallback,
            'errors': stats.errors,
            'start_time': stats.start_time.isoformat(),
            'end_time': stats.end_time.isoformat() if stats.end_time else None,
            'success_rate': (stats.total_records - stats.errors) / stats.total_records if stats.total_records > 0 else 0
        }
