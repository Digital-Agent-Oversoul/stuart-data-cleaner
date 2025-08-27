"""
Uncertainty Detection System

This module implements the uncertainty detection logic that identifies when the LLM
is unsure about data parsing decisions. It triggers interactive prompts for human
guidance on edge cases.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from .llm_engine import LLMResponse
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class UncertaintyCase:
    """Represents a case where the LLM is uncertain"""
    record_id: str
    contact_name: str
    customer_name: str
    email: str
    llm_response: LLMResponse
    uncertainty_type: str
    confidence_score: float
    context: Dict[str, Any]
    suggested_resolution: Optional[str] = None

class UncertaintyDetector:
    """
    Detects when the LLM is uncertain about data parsing decisions
    and triggers interactive prompts for human guidance.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the uncertainty detector
        
        Args:
            config: Configuration dictionary with uncertainty thresholds and rules
        """
        self.config = config
        
        # Uncertainty thresholds
        self.low_confidence_threshold = config.get('uncertainty', {}).get('low_confidence_threshold', 0.6)
        self.very_low_confidence_threshold = config.get('uncertainty', {}).get('very_low_confidence_threshold', 0.4)
        
        # Business name patterns that indicate uncertainty
        self.business_indicators = self._load_business_indicators()
        
        # Edge case patterns that often cause uncertainty
        self.edge_case_patterns = self._load_edge_case_patterns()
        
        # Uncertainty tracking
        self.uncertainty_cases: List[UncertaintyCase] = []
        self.resolved_patterns: Dict[str, Any] = {}
        
    def _load_business_indicators(self) -> Set[str]:
        """Load business name indicators that often cause confusion"""
        return {
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
        }
    
    def _load_edge_case_patterns(self) -> Dict[str, re.Pattern]:
        """Load regex patterns for edge cases that often cause uncertainty"""
        return {
            'multiple_names': re.compile(r'&|\band\b|\+', re.IGNORECASE),
            'hyphenated_names': re.compile(r'\w+\s*-\s*\w+'),
            'initials_only': re.compile(r'^[A-Z]\s*[A-Z]?\s*[A-Z]?$'),
            'business_like': re.compile(r'\b(?:LLC|INC|CORP|GROUP|CENTER|RESTAURANT|SCHOOL|CHURCH|UNIVERSITY|COLLEGE|HOSPITAL|CLINIC|FOUNDATION|ASSOCIATION|ORGANIZATION|INSTITUTE|SYSTEM|NETWORK|PARTNERS|ALLIANCE|PRODUCTIONS|STEAKHOUSE|WINE BAR|INNOVATION|TECHNOLOGY|REAL ESTATE|BOOSTER CLUB|TRADITION|RESIDENCE|DISTRICT|COUNTY|OFFICE|DEPARTMENT|DIVISION|BUREAU|AGENCY|AUTHORITY|COMMISSION|BOARD|COUNCIL|COMMITTEE|TEAM|STAFF|PERSONNEL|EMPLOYEES|WORKERS|MEMBERS|VOLUNTEERS|CAPITAL|MODERN|SENIOR|LIVING|ELEMENTARY|SOLUTIONS|SYSTEMS|INNOVATIONS|RESEARCH|CORPORATION|PRINT|DESIGN|DECOR|TILE|KITCHEN|CREATIONS|STREAMLINE|EXPECTATIONS|SUCCULENT|CACTUS|CLIMATE|WEEK|ZOO|HOTEL|CAFE|DELI|PLAZA|GYMNASTICS|GOVERNMENT|CITY|ARENA|AMERICAS|SOUTHERN|CLOUD|WEST|PACIFIC|LUXE|REAL-TIME)\b', re.IGNORECASE),
            'email_uncertainty': re.compile(r'\b(?:info|sales|support|admin|noreply|workplace-support|help|contact|service)@', re.IGNORECASE),
            'ambiguous_format': re.compile(r'^[A-Z\s]+$'),  # All caps text
            'very_long_name': re.compile(r'^.{30,}$'),  # Very long names
            'mixed_case_uncertainty': re.compile(r'^[A-Z][a-z]+[A-Z][a-z]+$')  # Mixed case patterns
        }
    
    def detect_uncertainty(self, record_id: str, contact_name: str, customer_name: str, 
                          email: str, llm_response: LLMResponse) -> Optional[UncertaintyCase]:
        """
        Detect if the LLM response indicates uncertainty
        
        Args:
            record_id: Unique identifier for the record
            contact_name: Contact name from the data
            customer_name: Customer name from the data
            email: Email address from the data
            llm_response: Response from the LLM engine
            
        Returns:
            UncertaintyCase if uncertainty detected, None otherwise
        """
        # Check confidence score
        if llm_response.confidence <= self.very_low_confidence_threshold:
            return self._create_uncertainty_case(
                record_id, contact_name, customer_name, email, llm_response,
                'very_low_confidence', llm_response.confidence
            )
        
        if llm_response.confidence <= self.low_confidence_threshold:
            return self._create_uncertainty_case(
                record_id, contact_name, customer_name, email, llm_response,
                'low_confidence', llm_response.confidence
            )
        
        # Check for specific uncertainty patterns
        uncertainty_type = self._check_uncertainty_patterns(contact_name, customer_name, email, llm_response)
        if uncertainty_type:
            return self._create_uncertainty_case(
                record_id, contact_name, customer_name, email, llm_response,
                uncertainty_type, llm_response.confidence
            )
        
        # Check for business vs person confusion
        if self._is_business_person_confusion(contact_name, customer_name, email, llm_response):
            return self._create_uncertainty_case(
                record_id, contact_name, customer_name, email, llm_response,
                'business_person_confusion', llm_response.confidence
            )
        
        # Check for edge case patterns
        edge_case_type = self._check_edge_case_patterns(contact_name, customer_name, email)
        if edge_case_type:
            return self._create_uncertainty_case(
                record_id, contact_name, customer_name, email, llm_response,
                edge_case_type, llm_response.confidence
            )
        
        return None
    
    def _create_uncertainty_case(self, record_id: str, contact_name: str, customer_name: str,
                                email: str, llm_response: LLMResponse, uncertainty_type: str,
                                confidence_score: float) -> UncertaintyCase:
        """Create an uncertainty case for human review"""
        
        context = {
            'contact_name_original': contact_name,
            'customer_name_original': customer_name,
            'email_original': email,
            'llm_first_name': llm_response.first_name,
            'llm_last_name': llm_response.last_name,
            'processing_method': llm_response.processing_method,
            'metadata': llm_response.metadata
        }
        
        # Generate suggested resolution based on uncertainty type
        suggested_resolution = self._generate_suggested_resolution(
            uncertainty_type, contact_name, customer_name, email, llm_response
        )
        
        uncertainty_case = UncertaintyCase(
            record_id=record_id,
            contact_name=contact_name,
            customer_name=customer_name,
            email=email,
            llm_response=llm_response,
            uncertainty_type=uncertainty_type,
            confidence_score=confidence_score,
            context=context,
            suggested_resolution=suggested_resolution
        )
        
        # Add to tracking
        self.uncertainty_cases.append(uncertainty_case)
        
        logger.info(f"Uncertainty detected for record {record_id}: {uncertainty_type} (confidence: {confidence_score:.2f})")
        
        return uncertainty_case
    
    def _check_uncertainty_patterns(self, contact_name: str, customer_name: str, 
                                  email: str, llm_response: LLMResponse) -> Optional[str]:
        """Check for specific patterns that indicate uncertainty"""
        
        # Check if LLM returned null for both names
        if not llm_response.first_name and not llm_response.last_name:
            return 'null_names_returned'
        
        # Check if only one name was extracted
        if bool(llm_response.first_name) != bool(llm_response.last_name):
            return 'incomplete_name_extraction'
        
        # Check for processing method failures
        if llm_response.processing_method in ['failed', 'error']:
            return 'processing_method_failure'
        
        # Check for very low confidence despite successful processing
        if llm_response.success and llm_response.confidence < 0.5:
            return 'low_confidence_despite_success'
        
        return None
    
    def _is_business_person_confusion(self, contact_name: str, customer_name: str,
                                    email: str, llm_response: LLMResponse) -> bool:
        """Check if there's confusion between business and person names"""
        
        # Check if contact name contains business indicators
        if contact_name:
            contact_lower = contact_name.lower()
            if any(indicator in contact_lower for indicator in self.business_indicators):
                # But LLM still extracted person names
                if llm_response.first_name or llm_response.last_name:
                    return True
        
        # Check if customer name is clearly business but contact name is person
        if customer_name:
            customer_lower = customer_name.lower()
            if any(indicator in customer_lower for indicator in self.business_indicators):
                if contact_name and not any(indicator in contact_name.lower() for indicator in self.business_indicators):
                    return True
        
        return False
    
    def _check_edge_case_patterns(self, contact_name: str, customer_name: str, email: str) -> Optional[str]:
        """Check for edge case patterns that often cause uncertainty"""
        
        # Check multiple names pattern
        if contact_name and self.edge_case_patterns['multiple_names'].search(contact_name):
            return 'multiple_names_detected'
        
        # Check hyphenated names
        if contact_name and self.edge_case_patterns['hyphenated_names'].search(contact_name):
            return 'hyphenated_name_pattern'
        
        # Check initials only
        if contact_name and self.edge_case_patterns['initials_only'].match(contact_name.strip()):
            return 'initials_only_name'
        
        # Check business-like patterns
        if contact_name and self.edge_case_patterns['business_like'].search(contact_name):
            return 'business_like_pattern'
        
        # Check email uncertainty
        if email and self.edge_case_patterns['email_uncertainty'].search(email):
            return 'business_email_pattern'
        
        # Check ambiguous format
        if contact_name and self.edge_case_patterns['ambiguous_format'].match(contact_name.strip()):
            return 'ambiguous_format'
        
        # Check very long names
        if contact_name and self.edge_case_patterns['very_long_name'].match(contact_name.strip()):
            return 'very_long_name'
        
        return None
    
    def _generate_suggested_resolution(self, uncertainty_type: str, contact_name: str,
                                     customer_name: str, email: str, llm_response: LLMResponse) -> Optional[str]:
        """Generate a suggested resolution for the uncertainty case"""
        
        if uncertainty_type == 'multiple_names_detected':
            return f"Multiple names detected in '{contact_name}'. Please specify which person to use for this record."
        
        elif uncertainty_type == 'business_person_confusion':
            return f"Potential confusion between business name '{customer_name}' and person name '{contact_name}'. Please clarify if this should be treated as a person or business record."
        
        elif uncertainty_type == 'hyphenated_name_pattern':
            return f"Hyphenated name detected in '{contact_name}'. Please confirm the correct formatting and which parts should be first vs last name."
        
        elif uncertainty_type == 'initials_only_name':
            return f"Only initials found in '{contact_name}'. Please provide the full name if available, or confirm if initials are sufficient."
        
        elif uncertainty_type == 'business_email_pattern':
            return f"Business email pattern detected in '{email}'. Please confirm if this should be treated as a person record despite the business email."
        
        elif uncertainty_type == 'null_names_returned':
            return f"No names could be extracted from the provided data. Please manually review and provide the correct person name."
        
        elif uncertainty_type == 'incomplete_name_extraction':
            return f"Only partial name extracted. Please provide the missing name component or confirm if partial information is acceptable."
        
        return f"Uncertainty detected in processing. Please review the data and provide guidance on how to handle this case."
    
    def get_uncertainty_summary(self) -> Dict[str, Any]:
        """Get a summary of all uncertainty cases"""
        if not self.uncertainty_cases:
            return {'total_cases': 0, 'cases': []}
        
        # Group by uncertainty type
        type_counts = {}
        for case in self.uncertainty_cases:
            uncertainty_type = case.uncertainty_type
            type_counts[uncertainty_type] = type_counts.get(uncertainty_type, 0) + 1
        
        # Calculate average confidence
        avg_confidence = sum(case.confidence_score for case in self.uncertainty_cases) / len(self.uncertainty_cases)
        
        return {
            'total_cases': len(self.uncertainty_cases),
            'type_counts': type_counts,
            'average_confidence': avg_confidence,
            'cases': [
                {
                    'record_id': case.record_id,
                    'uncertainty_type': case.uncertainty_type,
                    'confidence_score': case.confidence_score,
                    'suggested_resolution': case.suggested_resolution
                }
                for case in self.uncertainty_cases
            ]
        }
    
    def resolve_uncertainty_case(self, record_id: str, resolution: Dict[str, Any]) -> bool:
        """
        Resolve an uncertainty case with human guidance
        
        Args:
            record_id: ID of the record to resolve
            resolution: Human-provided resolution data
            
        Returns:
            True if resolved successfully, False otherwise
        """
        # Find the uncertainty case
        case = next((c for c in self.uncertainty_cases if c.record_id == record_id), None)
        if not case:
            logger.warning(f"Uncertainty case not found for record {record_id}")
            return False
        
        # Store the resolution pattern for future learning
        pattern_key = f"{case.uncertainty_type}_{case.contact_name}_{case.customer_name}_{case.email}"
        self.resolved_patterns[pattern_key] = {
            'resolution': resolution,
            'original_case': case,
            'resolved_at': datetime.now().isoformat()
        }
        
        # Remove from active uncertainty cases
        self.uncertainty_cases = [c for c in self.uncertainty_cases if c.record_id != record_id]
        
        logger.info(f"Uncertainty case resolved for record {record_id}")
        return True
    
    def should_prompt_for_guidance(self, uncertainty_case: UncertaintyCase) -> bool:
        """
        Determine if this uncertainty case should prompt for human guidance
        
        Args:
            uncertainty_case: The uncertainty case to evaluate
            
        Returns:
            True if human guidance should be requested, False otherwise
        """
        # Always prompt for very low confidence cases
        if uncertainty_case.confidence_score <= self.very_low_confidence_threshold:
            return True
        
        # Prompt for business-person confusion cases
        if uncertainty_case.uncertainty_type == 'business_person_confusion':
            return True
        
        # Prompt for multiple names cases
        if uncertainty_case.uncertainty_type == 'multiple_names_detected':
            return True
        
        # Prompt for null names cases
        if uncertainty_case.uncertainty_type == 'null_names_returned':
            return True
        
        # For other cases, use confidence threshold
        return uncertainty_case.confidence_score <= self.low_confidence_threshold
    
    def get_learning_patterns(self) -> Dict[str, Any]:
        """Get patterns learned from resolved uncertainty cases"""
        return {
            'total_resolved': len(self.resolved_patterns),
            'patterns': self.resolved_patterns
        }
    
    def reset_uncertainty_tracking(self):
        """Reset uncertainty tracking for new processing run"""
        self.uncertainty_cases = []
        # Keep resolved patterns for learning
