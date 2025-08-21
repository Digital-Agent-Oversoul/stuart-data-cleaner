"""
Contact Export Workflow Module

This module implements the Contact Export workflow using the core data cleaning engine.
It handles aggregated, larger outputs for monthly/quarterly contact processing.
"""

from .export_processor import ExportProcessor

__all__ = [
    'ExportProcessor'
]
