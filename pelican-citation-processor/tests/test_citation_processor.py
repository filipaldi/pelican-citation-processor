"""
Tests for the Pelican Citation Processor plugin.
"""

import os
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch, mock_open
from pelican.plugins.citation_processor import process_citations


class TestCitationProcessor(unittest.TestCase):
    """Test cases for the citation processor plugin."""

    def setUp(self):
        """Set up test fixtures."""
        self.article_generator = Mock()
        self.content = Mock()
        self.settings = Mock()
        self.article_generator.settings = self.settings

    def test_process_citations_no_content(self):
        """Test that processing is skipped when content has no _content attribute."""
        self.content._content = None
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = ""
        process_citations(self.article_generator, self.content)
        self.assertIsNone(self.content._content)

    def test_process_citations_no_citation_style(self):
        """Test that processing is skipped when CITATION_STYLE is not set."""
        self.content._content = "<p>Test content</p>"
        self.settings.CITATION_STYLE = None
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        
        process_citations(self.article_generator, self.content)
        
        self.assertEqual(self.content._content, "<p>Test content</p>")

    def test_process_citations_no_bibliography_file(self):
        """Test that processing is skipped when BIBLIOGRAPHY_FILE is not set."""
        self.content._content = "<p>Test content</p>"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = None
        
        process_citations(self.article_generator, self.content)
        
        self.assertEqual(self.content._content, "<p>Test content</p>")

    @patch('os.path.exists')
    def test_process_citations_bibliography_file_not_found(self, mock_exists):
        """Test that processing is skipped when bibliography file doesn't exist."""
        self.content._content = "<p>Test content</p>"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = ""
        mock_exists.return_value = False
        
        process_citations(self.article_generator, self.content)
        
        self.assertEqual(self.content._content, "<p>Test content</p>")

    @patch('os.path.exists')
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    def test_process_citations_success(self, mock_tempfile, mock_run, mock_exists):
        """Test successful citation processing."""
        self.content._content = "<p>Test content with [@citation]</p>"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = ""
        mock_exists.return_value = True
        
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

    @patch('os.path.exists')
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    def test_process_citations_pandoc_error(self, mock_tempfile, mock_run, mock_exists):
        """Test handling of Pandoc processing errors."""
        self.content._content = "<p>Test content with [@citation]</p>"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = ""
        mock_exists.return_value = True
        
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

    @patch('os.path.exists')
    @patch('tempfile.NamedTemporaryFile')
    def test_process_citations_temp_file_cleanup(self, mock_tempfile, mock_exists):
        """Test that temporary files are cleaned up properly."""
        self.content._content = "<p>Test content</p>"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = ""
        mock_exists.return_value = True
        
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