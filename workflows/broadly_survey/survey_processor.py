"""
Survey Processor Implementation

This module implements the Broadly Survey workflow processor using the core data cleaning engine.
It handles location-segmented, smaller outputs for daily survey processing.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.data_processor import DataProcessor
from core.llm_engine import LLMEngine
from core.name_parser import NameParser


class SurveyProcessor:
    """
    Broadly Survey workflow processor
    
    Handles daily survey data processing with location segmentation
    and smaller, focused outputs.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        # Transform config structure to match LLM engine expectations
        llm_config = {
            'openai': config.get('llm', {}),
            'ollama': config.get('llm', {})
        }
        self.llm_engine = LLMEngine(llm_config)
        self.name_parser = NameParser(self.llm_engine)
        self.data_processor = DataProcessor(config)
        
    def process_survey_data(self, data: pd.DataFrame, location_filter: Optional[str] = None) -> pd.DataFrame:
        """
        Process survey data with location-based filtering
        
        Args:
            data: Raw survey data
            location_filter: Optional location to filter by
            
        Returns:
            Processed survey data
        """
        # Apply location filtering if specified
        if location_filter:
            data = data[data['location'].str.contains(location_filter, case=False, na=False)]
            
        # Process using core engine
        processed_data = self.data_processor.process_survey_data(data)
        
        return processed_data
        
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            'llm_stats': self.llm_engine.get_stats(),
            'data_stats': self.data_processor.get_processing_stats()
        }
