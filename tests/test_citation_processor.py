"""
Tests for the Pelican Citation Processor plugin.
"""

import os
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch, mock_open
from pelican.plugins.citation_processor.citation_processor import process_citations, resolve_citation_config, resolve_file_path


class TestCitationProcessor(unittest.TestCase):
    """Test cases for the citation processor plugin."""

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

    @patch('os.path.isabs')
    @patch('os.path.exists')
    def test_resolve_file_path_absolute(self, mock_exists, mock_isabs):
        """Test file path resolution for absolute paths."""
        mock_isabs.return_value = True
        mock_exists.return_value = True
        
        result = resolve_file_path("/base", "/absolute/path/file.txt", self.settings)
        
        self.assertEqual(result, "/absolute/path/file.txt")

    @patch('os.path.isabs')
    @patch('os.path.exists')
    def test_resolve_file_path_relative_content(self, mock_exists, mock_isabs):
        """Test file path resolution for relative paths in content directory."""
        mock_isabs.return_value = False
        mock_exists.side_effect = [True, False]
        
        result = resolve_file_path("/content", "file.txt", self.settings)
        
        self.assertEqual(result, "/content/file.txt")

    @patch('os.path.isabs')
    @patch('os.path.exists')
    def test_resolve_file_path_relative_settings(self, mock_exists, mock_isabs):
        """Test file path resolution for relative paths in settings PATH."""
        mock_isabs.return_value = False
        mock_exists.side_effect = [False, True]
        self.settings.get.return_value = "/settings"
        
        result = resolve_file_path("/content", "file.txt", self.settings)
        
        self.assertEqual(result, "/settings/file.txt")

    @patch('os.path.isabs')
    @patch('os.path.exists')
    def test_resolve_file_path_fallback(self, mock_exists, mock_isabs):
        """Test file path resolution fallback to content directory."""
        mock_isabs.return_value = False
        mock_exists.return_value = False
        self.settings.get.return_value = "/settings"
        
        result = resolve_file_path("/content", "file.txt", self.settings)
        
        self.assertEqual(result, "/content/file.txt")

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    def test_process_citations_no_content(self, mock_resolve_config):
        """Test that processing is skipped when content has no _content attribute."""
        self.content._content = None
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = ""
        process_citations(self.article_generator, self.content)
        self.assertIsNone(self.content._content)

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    def test_process_citations_no_citation_style(self, mock_resolve_config):
        """Test that processing is skipped when CITATION_STYLE is not set."""
        self.content._content = "<p>Test content</p>"
        self.settings.CITATION_STYLE = None
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        
        mock_resolve_config.return_value = {'citation_style': None, 'bibliography_file': '_bibliography.bib'}
        
        process_citations(self.article_generator, self.content)
        
        self.assertEqual(self.content._content, "<p>Test content</p>")

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    def test_process_citations_no_bibliography_file(self, mock_resolve_config):
        """Test that processing is skipped when BIBLIOGRAPHY_FILE is not set."""
        self.content._content = "<p>Test content</p>"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = None
        
        mock_resolve_config.return_value = {'citation_style': 'style.csl', 'bibliography_file': None}
        
        process_citations(self.article_generator, self.content)
        
        self.assertEqual(self.content._content, "<p>Test content</p>")

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    @patch('os.path.exists')
    def test_process_citations_bibliography_file_not_found(self, mock_exists, mock_resolve_config):
        """Test that processing is skipped when bibliography file doesn't exist."""
        self.content._content = "<p>Test content</p>"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = ""
        mock_exists.return_value = False
        mock_resolve_config.return_value = {'citation_style': 'style.csl', 'bibliography_file': '_bibliography.bib'}
        
        with patch('builtins.print') as mock_print:
            process_citations(self.article_generator, self.content)
        
        mock_print.assert_called()
        self.assertEqual(self.content._content, "<p>Test content</p>")

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    @patch('os.path.exists')
    def test_process_citations_csl_file_not_found(self, mock_exists, mock_resolve_config):
        """Test that processing is skipped when CSL file doesn't exist."""
        self.content._content = "<p>Test content</p>"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = ""
        mock_exists.side_effect = [True, False, False, False]
        mock_resolve_config.return_value = {'citation_style': 'style.csl', 'bibliography_file': '_bibliography.bib'}
        
        with patch('builtins.print') as mock_print:
            process_citations(self.article_generator, self.content)
        
        mock_print.assert_called()
        self.assertEqual(self.content._content, "<p>Test content</p>")

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    @patch('os.path.exists')
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    def test_process_citations_success(self, mock_tempfile, mock_run, mock_exists, mock_resolve_config):
        """Test successful citation processing."""
        self.content._content = "<p>Test content with [@citation]</p>"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = ""
        mock_exists.return_value = True
        mock_resolve_config.return_value = {'citation_style': 'style.csl', 'bibliography_file': '_bibliography.bib'}
        
        mock_input_file = Mock()
        mock_input_file.name = "/tmp/input.html"
        mock_input_file.__enter__ = Mock(return_value=mock_input_file)
        mock_input_file.__exit__ = Mock(return_value=None)
        
        mock_output_file = Mock()
        mock_output_file.name = "/tmp/output.html"
        mock_output_file.__enter__ = Mock(return_value=mock_output_file)
        mock_output_file.__exit__ = Mock(return_value=None)
        
        mock_tempfile.side_effect = [mock_input_file, mock_output_file]
        
        mock_run.return_value = Mock(returncode=0)
        
        with patch('builtins.open', mock_open(read_data="<p>Processed content</p>")):
            process_citations(self.article_generator, self.content)
        
        self.assertEqual(self.content._content, "<p>Processed content</p>")
        mock_run.assert_called_once()

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    @patch('os.path.exists')
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    def test_process_citations_with_local_config(self, mock_tempfile, mock_run, mock_exists, mock_resolve_config):
        """Test citation processing with local configuration."""
        self.content._content = "<p>Test content with [@citation]</p>"
        self.content.citation_style = "local_style.csl"
        self.content.bibliography_file = "local_bib.bib"
        
        self.settings.CITATION_STYLE = "global_style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "global_bib.bib"
        self.settings.get.return_value = ""
        mock_exists.return_value = True
        mock_resolve_config.return_value = {'citation_style': 'local_style.csl', 'bibliography_file': 'local_bib.bib'}
        
        mock_input_file = Mock()
        mock_input_file.name = "/tmp/input.html"
        mock_input_file.__enter__ = Mock(return_value=mock_input_file)
        mock_input_file.__exit__ = Mock(return_value=None)
        
        mock_output_file = Mock()
        mock_output_file.name = "/tmp/output.html"
        mock_output_file.__enter__ = Mock(return_value=mock_output_file)
        mock_output_file.__exit__ = Mock(return_value=None)
        
        mock_tempfile.side_effect = [mock_input_file, mock_output_file]
        
        mock_run.return_value = Mock(returncode=0)
        
        with patch('builtins.open', mock_open(read_data="<p>Processed content</p>")):
            process_citations(self.article_generator, self.content)
        
        self.assertEqual(self.content._content, "<p>Processed content</p>")
        mock_run.assert_called_once()

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    @patch('os.path.exists')
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    def test_process_citations_pandoc_error(self, mock_tempfile, mock_run, mock_exists, mock_resolve_config):
        """Test handling of Pandoc processing errors."""
        self.content._content = "<p>Test content with [@citation]</p>"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = ""
        mock_exists.return_value = True
        mock_resolve_config.return_value = {'citation_style': 'style.csl', 'bibliography_file': '_bibliography.bib'}
        
        mock_input_file = Mock()
        mock_input_file.name = "/tmp/input.html"
        mock_input_file.__enter__ = Mock(return_value=mock_input_file)
        mock_input_file.__exit__ = Mock(return_value=None)
        
        mock_output_file = Mock()
        mock_output_file.name = "/tmp/output.html"
        mock_output_file.__enter__ = Mock(return_value=mock_output_file)
        mock_output_file.__exit__ = Mock(return_value=None)
        
        mock_tempfile.side_effect = [mock_input_file, mock_output_file]
        
        mock_run.side_effect = subprocess.CalledProcessError(1, "pandoc", stderr="Error")
        
        with patch('builtins.print') as mock_print:
            process_citations(self.article_generator, self.content)
        
        mock_print.assert_called()
        self.assertEqual(self.content._content, "<p>Test content with [@citation]</p>")

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    @patch('os.path.exists')
    @patch('tempfile.NamedTemporaryFile')
    def test_process_citations_temp_file_cleanup(self, mock_tempfile, mock_exists, mock_resolve_config):
        """Test that temporary files are cleaned up properly."""
        self.content._content = "<p>Test content</p>"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = ""
        mock_exists.return_value = True
        mock_resolve_config.return_value = {'citation_style': 'style.csl', 'bibliography_file': '_bibliography.bib'}
        
        mock_input_file = Mock()
        mock_input_file.name = "/tmp/input.html"
        mock_input_file.__enter__ = Mock(return_value=mock_input_file)
        mock_input_file.__exit__ = Mock(return_value=None)
        
        mock_output_file = Mock()
        mock_output_file.name = "/tmp/output.html"
        mock_output_file.__enter__ = Mock(return_value=mock_output_file)
        mock_output_file.__exit__ = Mock(return_value=None)
        
        mock_tempfile.side_effect = [mock_input_file, mock_output_file]
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = Exception("Test exception")
            with patch('os.unlink') as mock_unlink:
                process_citations(self.article_generator, self.content)
                mock_unlink.assert_called()


if __name__ == '__main__':
    unittest.main() 