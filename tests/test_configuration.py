"""
Tests for configuration resolution in the Pelican Citation Processor plugin.
"""

import unittest
from unittest.mock import Mock
from pelican.plugins.citation_processor.citation_processor import (
    resolve_citation_config,
    resolve_processing_config
)


class TestConfiguration(unittest.TestCase):
    """Test cases for configuration resolution."""

    def setUp(self):
        """Set up test fixtures."""
        self.article_generator = Mock()
        self.content = Mock()
        self.settings = Mock()
        self.article_generator.settings = self.settings

    def test_resolve_citation_config_global_only(self):
        """Test configuration resolution with global settings only."""
        self.settings.CITATION_STYLE = "global_style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "global_bib.bib"
        
        # Ensure Mock objects return the correct values
        self.content.citation_style = None
        self.content.bibliography_file = None
        
        config = resolve_citation_config(self.article_generator, self.content)
        
        self.assertEqual(config['citation_style'], "global_style.csl")
        self.assertEqual(config['bibliography_file'], "global_bib.bib")

    def test_resolve_citation_config_local_override(self):
        """Test that local settings override global settings."""
        self.settings.CITATION_STYLE = "global_style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "global_bib.bib"
        
        self.content.citation_style = "local_style.csl"
        self.content.bibliography_file = "local_bib.bib"
        
        config = resolve_citation_config(self.article_generator, self.content)
        
        self.assertEqual(config['citation_style'], "local_style.csl")
        self.assertEqual(config['bibliography_file'], "local_bib.bib")

    def test_resolve_citation_config_mixed(self):
        """Test configuration resolution with mixed global and local settings."""
        self.settings.CITATION_STYLE = "global_style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "global_bib.bib"
        
        self.content.citation_style = "local_style.csl"
        self.content.bibliography_file = None
        
        config = resolve_citation_config(self.article_generator, self.content)
        
        self.assertEqual(config['citation_style'], "local_style.csl")
        self.assertEqual(config['bibliography_file'], "global_bib.bib")

    def test_resolve_citation_config_default_bibliography(self):
        """Test that default bibliography file is used when not specified."""
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        
        # Ensure Mock objects return the correct values
        self.content.citation_style = None
        self.content.bibliography_file = None
        
        config = resolve_citation_config(self.article_generator, self.content)
        
        self.assertEqual(config['citation_style'], "style.csl")
        self.assertEqual(config['bibliography_file'], "_bibliography.bib")

    def test_resolve_processing_config_defaults(self):
        """Test processing configuration resolution with defaults."""
        self.settings.CITATION_PROCESSING_MODE = None
        self.settings.CITATION_FALLBACK_TO_HTML = None
        
        config = resolve_processing_config(self.article_generator)
        
        self.assertEqual(config['processing_mode'], 'markdown')
        self.assertEqual(config['fallback_to_html'], True)

    def test_resolve_processing_config_explicit(self):
        """Test processing configuration resolution with explicit settings."""
        self.settings.CITATION_PROCESSING_MODE = 'html'
        self.settings.CITATION_FALLBACK_TO_HTML = False
        
        config = resolve_processing_config(self.article_generator)
        
        self.assertEqual(config['processing_mode'], 'html')
        self.assertEqual(config['fallback_to_html'], False)

    def test_resolve_processing_config_auto_mode(self):
        """Test processing configuration resolution with auto mode."""
        self.settings.CITATION_PROCESSING_MODE = 'auto'
        self.settings.CITATION_FALLBACK_TO_HTML = True
        
        config = resolve_processing_config(self.article_generator)
        
        self.assertEqual(config['processing_mode'], 'auto')
        self.assertEqual(config['fallback_to_html'], True)


if __name__ == '__main__':
    unittest.main() 