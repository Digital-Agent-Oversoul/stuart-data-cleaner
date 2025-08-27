"""
Configuration Module for Unified Data Cleaner

This module provides default configuration settings and configuration management
for the unified data cleaning system.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class LLMConfig:
    """Configuration for LLM services"""
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    openai_base_url: Optional[str] = None
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b-instruct-q4_K_M"
    max_tokens: int = 1000
    temperature: float = 0.1
    timeout_seconds: int = 30

@dataclass
class BudgetConfig:
    """Configuration for budget monitoring"""
    openai_cost_per_1k_tokens: float = 0.00015  # gpt-4o-mini pricing
    max_daily_cost: float = 5.0
    max_total_cost: float = 50.0
    warn_at_percentage: float = 0.8

@dataclass
class ProcessingConfig:
    """Configuration for data processing"""
    batch_size: int = 50
    max_workers: int = 4
    confidence_threshold: float = 0.3
    enable_uncertainty_detection: bool = True
    enable_interactive_learning: bool = True
    show_progress: bool = True
    max_retries: int = 3
    retry_delay_ms: int = 1000

@dataclass
class UncertaintyConfig:
    """Configuration for uncertainty detection"""
    low_confidence_threshold: float = 0.6
    very_low_confidence_threshold: float = 0.4
    enable_business_detection: bool = True
    enable_edge_case_detection: bool = True

@dataclass
class OutputConfig:
    """Configuration for output handling"""
    output_directory: str = "output"
    backup_original: bool = True
    create_summary_report: bool = True
    enable_progress_tracking: bool = True

class Config:
    """Main configuration class for the unified data cleaner"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            config_file: Optional path to configuration file
        """
        # Initialize sub-configurations first
        self.llm = LLMConfig()
        self.budget = BudgetConfig()
        self.processing = ProcessingConfig()
        self.uncertainty = UncertaintyConfig()
        self.output = OutputConfig()
        
        # Load environment variables
        self._load_environment_vars()
        
        # Load configuration file if provided, or try to load default config.json
        if config_file and os.path.exists(config_file):
            self._load_config_file(config_file)
        else:
            # Try to load default config.json in the same directory as this file
            default_config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            if os.path.exists(default_config_path):
                self._load_config_file(default_config_path)
        
        # Apply environment variable overrides (these take precedence)
        self._apply_env_overrides()
    
    def _load_environment_vars(self):
        """Load configuration from environment variables"""
        self.env_config = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'OPENAI_MODEL': os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            'OLLAMA_BASE_URL': os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
            'OLLAMA_MODEL': os.getenv('OLLAMA_MODEL', 'qwen2.5:7b-instruct-q4_K_M'),
            'MAX_DAILY_COST': os.getenv('MAX_DAILY_COST', '5.0'),
            'OUTPUT_DIRECTORY': os.getenv('OUTPUT_DIRECTORY', 'output'),
        }
    
    def _load_config_file(self, config_file: str):
        """Load configuration from JSON configuration file"""
        import json
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            # Load LLM configuration
            if 'llm' in config_data:
                llm_data = config_data['llm']
                if 'openai_api_key' in llm_data:
                    self.llm.openai_api_key = llm_data['openai_api_key']
                if 'openai_model' in llm_data:
                    self.llm.openai_model = llm_data['openai_model']
                if 'openai_base_url' in llm_data:
                    self.llm.openai_base_url = llm_data['openai_base_url']
                if 'ollama_base_url' in llm_data:
                    self.llm.ollama_base_url = llm_data['ollama_base_url']
                if 'ollama_model' in llm_data:
                    self.llm.ollama_model = llm_data['ollama_model']
                if 'max_tokens' in llm_data:
                    self.llm.max_tokens = llm_data['max_tokens']
                if 'temperature' in llm_data:
                    self.llm.temperature = llm_data['temperature']
                if 'timeout_seconds' in llm_data:
                    self.llm.timeout_seconds = llm_data['timeout_seconds']
            
            # Load budget configuration
            if 'budget' in config_data:
                budget_data = config_data['budget']
                if 'openai_cost_per_1k_tokens' in budget_data:
                    self.budget.openai_cost_per_1k_tokens = budget_data['openai_cost_per_1k_tokens']
                if 'max_daily_cost' in budget_data:
                    self.budget.max_daily_cost = budget_data['max_daily_cost']
                if 'max_total_cost' in budget_data:
                    self.budget.max_total_cost = budget_data['max_total_cost']
                if 'warn_at_percentage' in budget_data:
                    self.budget.warn_at_percentage = budget_data['warn_at_percentage']
            
            # Load processing configuration
            if 'processing' in config_data:
                processing_data = config_data['processing']
                if 'batch_size' in processing_data:
                    self.processing.batch_size = processing_data['batch_size']
                if 'max_workers' in processing_data:
                    self.processing.max_workers = processing_data['max_workers']
                if 'confidence_threshold' in processing_data:
                    self.processing.confidence_threshold = processing_data['confidence_threshold']
                if 'enable_uncertainty_detection' in processing_data:
                    self.processing.enable_uncertainty_detection = processing_data['enable_uncertainty_detection']
                if 'enable_interactive_learning' in processing_data:
                    self.processing.enable_interactive_learning = processing_data['enable_interactive_learning']
                if 'show_progress' in processing_data:
                    self.processing.show_progress = processing_data['show_progress']
                if 'max_retries' in processing_data:
                    self.processing.max_retries = processing_data['max_retries']
                if 'retry_delay_ms' in processing_data:
                    self.processing.retry_delay_ms = processing_data['retry_delay_ms']
            
            # Load uncertainty configuration
            if 'uncertainty' in config_data:
                uncertainty_data = config_data['uncertainty']
                if 'low_confidence_threshold' in uncertainty_data:
                    self.uncertainty.low_confidence_threshold = uncertainty_data['low_confidence_threshold']
                if 'very_low_confidence_threshold' in uncertainty_data:
                    self.uncertainty.very_low_confidence_threshold = uncertainty_data['very_low_confidence_threshold']
                if 'enable_business_detection' in uncertainty_data:
                    self.uncertainty.enable_business_detection = uncertainty_data['enable_business_detection']
                if 'enable_edge_case_detection' in uncertainty_data:
                    self.uncertainty.enable_edge_case_detection = uncertainty_data['enable_edge_case_detection']
            
            # Load output configuration
            if 'output' in config_data:
                output_data = config_data['output']
                if 'output_directory' in output_data:
                    self.output.output_directory = output_data['output_directory']
                if 'backup_original' in output_data:
                    self.output.backup_original = output_data['backup_original']
                if 'create_summary_report' in output_data:
                    self.output.create_summary_report = output_data['create_summary_report']
                if 'enable_progress_tracking' in output_data:
                    self.output.enable_progress_tracking = output_data['enable_progress_tracking']
                    
        except Exception as e:
            print(f"Warning: Could not load configuration file {config_file}: {e}")
            print("Using default configuration values.")
    
    def _apply_env_overrides(self):
        """Apply environment variable overrides to configuration"""
        # LLM configuration overrides
        if self.env_config.get('OPENAI_API_KEY'):
            self.llm.openai_api_key = self.env_config['OPENAI_API_KEY']
        if self.env_config.get('OPENAI_MODEL'):
            self.llm.openai_model = self.env_config['OPENAI_MODEL']
        if self.env_config.get('OLLAMA_BASE_URL'):
            self.llm.ollama_base_url = self.env_config['OLLAMA_BASE_URL']
        if self.env_config.get('OLLAMA_MODEL'):
            self.llm.ollama_model = self.env_config['OLLAMA_MODEL']
        
        # Budget configuration overrides
        if self.env_config.get('MAX_DAILY_COST'):
            try:
                self.budget.max_daily_cost = float(self.env_config['MAX_DAILY_COST'])
            except ValueError:
                logger.warning(f"Invalid MAX_DAILY_COST value: {self.env_config['MAX_DAILY_COST']}")
        
        # Processing configuration overrides
        if self.env_config.get('MAX_TOKENS'):
            try:
                self.llm.max_tokens = int(self.env_config['MAX_TOKENS'])
            except ValueError:
                logger.warning(f"Invalid MAX_TOKENS value: {self.env_config['MAX_TOKENS']}")
        
        if self.env_config.get('TEMPERATURE'):
            try:
                self.llm.temperature = float(self.env_config['TEMPERATURE'])
            except ValueError:
                logger.warning(f"Invalid TEMPERATURE value: {self.env_config['TEMPERATURE']}")
        
        if self.env_config.get('BATCH_SIZE'):
            try:
                self.processing.batch_size = int(self.env_config['BATCH_SIZE'])
            except ValueError:
                logger.warning(f"Invalid BATCH_SIZE value: {self.env_config['BATCH_SIZE']}")
        
        if self.env_config.get('MAX_WORKERS'):
            try:
                self.processing.max_workers = int(self.env_config['MAX_WORKERS'])
            except ValueError:
                logger.warning(f"Invalid MAX_WORKERS value: {self.env_config['MAX_WORKERS']}")
        
        # Output configuration overrides
        if self.env_config.get('OUTPUT_DIRECTORY'):
            self.output.output_directory = self.env_config['OUTPUT_DIRECTORY']
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration as dictionary"""
        return {
            'openai_api_key': self.llm.openai_api_key,
            'openai_model': self.llm.openai_model,
            'openai_base_url': self.llm.openai_base_url,
            'ollama_base_url': self.llm.ollama_base_url,
            'ollama_model': self.llm.ollama_model,
            'max_tokens': self.llm.max_tokens,
            'temperature': self.llm.temperature,
            'timeout_seconds': self.llm.timeout_seconds
        }
    
    def get_budget_config(self) -> Dict[str, Any]:
        """Get budget configuration as dictionary"""
        return {
            'openai_cost_per_1k_tokens': self.budget.openai_cost_per_1k_tokens,
            'max_daily_cost': self.budget.max_daily_cost,
            'max_total_cost': self.budget.max_total_cost,
            'warn_at_percentage': self.budget.warn_at_percentage
        }
    
    def get_processing_config(self) -> Dict[str, Any]:
        """Get processing configuration as dictionary"""
        return {
            'batch_size': self.processing.batch_size,
            'max_workers': self.processing.max_workers,
            'confidence_threshold': self.processing.confidence_threshold,
            'enable_uncertainty_detection': self.processing.enable_uncertainty_detection,
            'enable_interactive_learning': self.processing.enable_interactive_learning,
            'show_progress': self.processing.show_progress,
            'max_retries': self.processing.max_retries,
            'retry_delay_ms': self.processing.retry_delay_ms
        }
    
    def get_uncertainty_config(self) -> Dict[str, Any]:
        """Get uncertainty configuration as dictionary"""
        return {
            'low_confidence_threshold': self.uncertainty.low_confidence_threshold,
            'very_low_confidence_threshold': self.uncertainty.very_low_confidence_threshold,
            'enable_business_detection': self.uncertainty.enable_business_detection,
            'enable_edge_case_detection': self.uncertainty.enable_edge_case_detection
        }
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration as dictionary"""
        return {
            'output_directory': self.output.output_directory,
            'backup_original': self.output.backup_original,
            'create_summary_report': self.output.create_summary_report,
            'enable_progress_tracking': self.output.enable_progress_tracking
        }
    
    def get_full_config(self) -> Dict[str, Any]:
        """Get complete configuration as dictionary"""
        return {
            'llm': self.get_llm_config(),
            'budget': self.get_budget_config(),
            'processing': self.get_processing_config(),
            'uncertainty': self.get_uncertainty_config(),
            'output': self.get_output_config()
        }
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        errors = []
        
        # Check required settings
        if not self.llm.openai_api_key:
            errors.append("OpenAI API key is required")
        
        if not self.llm.ollama_base_url:
            errors.append("Ollama base URL is required")
        
        if self.budget.max_daily_cost <= 0:
            errors.append("Max daily cost must be positive")
        
        if self.processing.confidence_threshold < 0 or self.processing.confidence_threshold > 1:
            errors.append("Confidence threshold must be between 0 and 1")
        
        if self.uncertainty.low_confidence_threshold < 0 or self.uncertainty.low_confidence_threshold > 1:
            errors.append("Low confidence threshold must be between 0 and 1")
        
        if self.uncertainty.very_low_confidence_threshold < 0 or self.uncertainty.very_low_confidence_threshold > 1:
            errors.append("Very low confidence threshold must be between 0 and 1")
        
        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True

def get_default_config() -> Config:
    """Get default configuration instance"""
    return Config()

def get_config_from_env() -> Config:
    """Get configuration from environment variables only"""
    return Config()
