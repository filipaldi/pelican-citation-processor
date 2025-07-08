"""
Tests for the Pelican Citation Processor plugin.

Note: This file contains legacy tests for backward compatibility.
New tests are organized in separate files:
- test_configuration.py: Configuration resolution tests
- test_utils.py: Utility function tests  
- test_markdown_processing.py: Markdown citation processing tests
- test_html_processing.py: HTML citation processing tests
"""

import os
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch, mock_open
from pelican.plugins.citation_processor.citation_processor import (
    process_citations, 
    process_citations_markdown,
    process_citations_html_fallback,
    resolve_citation_config, 
    resolve_file_path,
    resolve_processing_config
)


class TestCitationProcessorLegacy(unittest.TestCase):
    """Legacy test cases for backward compatibility."""

    def setUp(self):
        """Set up test fixtures."""
        self.article_generator = Mock()
        self.content = Mock()
        self.settings = Mock()
        self.article_generator.settings = self.settings

    def test_resolve_citation_config_legacy(self):
        """Legacy test for configuration resolution."""
        self.settings.CITATION_STYLE = "global_style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "global_bib.bib"
        
        self.content.citation_style = None
        self.content.bibliography_file = None
        
        config = resolve_citation_config(self.article_generator, self.content)
        
        self.assertEqual(config['citation_style'], "global_style.csl")
        self.assertEqual(config['bibliography_file'], "global_bib.bib")

    def test_resolve_file_path_legacy(self):
        """Legacy test for file path resolution."""
        # This is a simple test to ensure the function exists and can be called
        result = resolve_file_path("/base", "/absolute/path/file.txt", self.settings)
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main() 