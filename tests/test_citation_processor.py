import os
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch, mock_open
from pelican.plugins.citation_processor.citation_processor import process_citations, resolve_citation_config, resolve_file_path


class TestCitationProcessorLegacy(unittest.TestCase):

    def setUp(self):
        self.article_generator = Mock()
        self.content = Mock()
        self.settings = Mock()
        self.article_generator.settings = self.settings

    def test_resolve_citation_config_legacy(self):
        self.settings.CITATION_STYLE = "global_style.csl"
        self.settings.BIBLIOGRAPHY_FILE = "global_bib.bib"
        
        self.content.citation_style = None
        self.content.bibliography_file = None
        
        config = resolve_citation_config(self.article_generator, self.content)
        
        self.assertEqual(config['citation_style'], "global_style.csl")
        self.assertEqual(config['bibliography_file'], "global_bib.bib")

    def test_resolve_file_path_legacy(self):
        with patch('os.path.isabs') as mock_isabs:
            with patch('os.path.exists') as mock_exists:
                mock_isabs.return_value = True
                mock_exists.return_value = True
                
                result = resolve_file_path("/base", "/absolute/path/file.txt", self.settings)
                
                self.assertEqual(result, "/absolute/path/file.txt")


if __name__ == '__main__':
    unittest.main() 