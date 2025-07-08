"""
Tests for Markdown citation processing in the Pelican Citation Processor plugin.
"""

import subprocess
import unittest
from unittest.mock import Mock, patch, mock_open
from pelican.plugins.citation_processor.citation_processor import process_citations


class TestMarkdownProcessing(unittest.TestCase):
    """Test cases for Markdown citation processing."""

    def setUp(self):
        """Set up test fixtures."""
        self.article_generator = Mock()
        self.content = Mock()
        self.settings = Mock()
        self.article_generator.settings = self.settings

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    @patch('os.path.exists')
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    def test_process_citations_success(self, mock_tempfile, mock_run, mock_exists, mock_resolve_config):
        self.content._content = "# Test Article\n\nThis is a test with [@citation] reference."
        self.content.source_path = "/content/test.md"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = "/content"
        mock_exists.return_value = True
        mock_resolve_config.return_value = {'citation_style': 'style.csl', 'bibliography_file': '_bibliography.bib'}
        
        mock_input_file = Mock()
        mock_input_file.name = "/tmp/input.md"
        mock_input_file.__enter__ = Mock(return_value=mock_input_file)
        mock_input_file.__exit__ = Mock(return_value=None)
        
        mock_output_file = Mock()
        mock_output_file.name = "/tmp/output.html"
        mock_output_file.__enter__ = Mock(return_value=mock_output_file)
        mock_output_file.__exit__ = Mock(return_value=None)
        
        mock_tempfile.side_effect = [mock_input_file, mock_output_file]
        
        mock_run.return_value = Mock(returncode=0)
        
        with patch('builtins.open', mock_open(read_data="<h1>Test Article</h1>\n<p>This is a test with <span class=\"citation\">citation</span> reference.</p>")):
            process_citations(self.article_generator, self.content)
        
        self.assertEqual(self.content._content, "<h1>Test Article</h1>\n<p>This is a test with <span class=\"citation\">citation</span> reference.</p>")
        mock_run.assert_called_once()

    def test_process_citations_no_content(self):
        self.content._content = None
        
        process_citations(self.article_generator, self.content)
        self.assertIsNone(self.content._content)

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    @patch('os.path.exists')
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    def test_process_citations_pandoc_error(self, mock_tempfile, mock_run, mock_exists, mock_resolve_config):
        self.content._content = "# Test Article\n\nThis is a test with [@citation] reference."
        self.content.source_path = "/content/test.md"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = "/content"
        mock_exists.return_value = True
        mock_resolve_config.return_value = {'citation_style': 'style.csl', 'bibliography_file': '_bibliography.bib'}
        
        mock_input_file = Mock()
        mock_input_file.name = "/tmp/input.md"
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

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    @patch('os.path.exists')
    def test_process_citations_missing_files(self, mock_exists, mock_resolve_config):
        self.content._content = "# Test Article\n\nThis is a test with [@citation] reference."
        self.content.source_path = "/content/test.md"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.get.return_value = "/content"
        mock_exists.return_value = False
        mock_resolve_config.return_value = {'citation_style': 'style.csl', 'bibliography_file': '_bibliography.bib'}
        
        with patch('builtins.print') as mock_print:
            process_citations(self.article_generator, self.content)
        
        mock_print.assert_called()

    @patch('pelican.plugins.citation_processor.citation_processor.resolve_citation_config')
    @patch('os.path.exists')
    @patch('subprocess.run')
    @patch('tempfile.NamedTemporaryFile')
    def test_process_citations_debug_logging(self, mock_tempfile, mock_run, mock_exists, mock_resolve_config):
        self.content._content = "# Test Article\n\nThis is a test with [@citation] reference."
        self.content.source_path = "/content/test.md"
        self.settings.CITATION_STYLE = "style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
        self.settings.DEBUG = True
        self.settings.get.return_value = "/content"
        mock_exists.return_value = True
        mock_resolve_config.return_value = {'citation_style': 'style.csl', 'bibliography_file': '_bibliography.bib'}
        
        mock_input_file = Mock()
        mock_input_file.name = "/tmp/input.md"
        mock_input_file.__enter__ = Mock(return_value=mock_input_file)
        mock_input_file.__exit__ = Mock(return_value=None)
        
        mock_output_file = Mock()
        mock_output_file.name = "/tmp/output.html"
        mock_output_file.__enter__ = Mock(return_value=mock_output_file)
        mock_output_file.__exit__ = Mock(return_value=None)
        
        mock_tempfile.side_effect = [mock_input_file, mock_output_file]
        
        mock_run.return_value = Mock(returncode=0)
        
        with patch('builtins.open', mock_open(read_data="<h1>Test Article</h1>\n<p>Processed content</p>")):
            with patch('builtins.print') as mock_print:
                process_citations(self.article_generator, self.content)
        
        mock_print.assert_called()


if __name__ == '__main__':
    unittest.main() 