"""
Configuration Module for Unified Data Cleaner

This module provides default configuration settings and configuration management
for the unified data cleaning system.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

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
        # Load environment variables
        self._load_environment_vars()
        
        # Load configuration file if provided
        if config_file and os.path.exists(config_file):
            self._load_config_file(config_file)
        
        # Initialize sub-configurations
        self.llm = LLMConfig()
        self.budget = BudgetConfig()
        self.processing = ProcessingConfig()
        self.uncertainty = UncertaintyConfig()
        self.output = OutputConfig()
        
        # Apply environment variable overrides
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
        """Load configuration from file (placeholder for future implementation)"""
        # TODO: Implement JSON/YAML configuration file loading
        pass
    
    def _apply_env_overrides(self):
        """Apply environment variable overrides to configuration"""
        if self.env_config['OPENAI_API_KEY']:
            self.llm.openai_api_key = self.env_config['OPENAI_API_KEY']
        
        if self.env_config['OPENAI_MODEL']:
            self.llm.openai_model = self.env_config['OPENAI_MODEL']
        
        if self.env_config['OLLAMA_BASE_URL']:
            self.llm.ollama_base_url = self.env_config['OLLAMA_BASE_URL']
        
        if self.env_config['OLLAMA_MODEL']:
            self.llm.ollama_model = self.env_config['OLLAMA_MODEL']
        
        if self.env_config['MAX_DAILY_COST']:
            self.budget.max_daily_cost = float(self.env_config['MAX_DAILY_COST'])
        
        if self.env_config['OUTPUT_DIRECTORY']:
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
            'enable_interactive_learning': self.processing.enable_interactive_learning
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
