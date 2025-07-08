import unittest
from unittest.mock import Mock, patch
from pelican.plugins.citation_processor.citation_processor import resolve_file_path


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.settings = Mock()

    @patch('os.path.isabs')
    @patch('os.path.exists')
    def test_resolve_file_path_absolute(self, mock_exists, mock_isabs):
        mock_isabs.return_value = True
        mock_exists.return_value = True
        
        result = resolve_file_path("/base", "/absolute/path/file.txt", self.settings)
        
        self.assertEqual(result, "/absolute/path/file.txt")

    @patch('os.path.isabs')
    @patch('os.path.exists')
    def test_resolve_file_path_relative_content(self, mock_exists, mock_isabs):
        mock_isabs.return_value = False
        mock_exists.side_effect = [True, False]
        
        result = resolve_file_path("/content", "file.txt", self.settings)
        
        self.assertEqual(result, "/content/file.txt")

    @patch('os.path.isabs')
    @patch('os.path.exists')
    def test_resolve_file_path_relative_settings(self, mock_exists, mock_isabs):
        mock_isabs.return_value = False
        mock_exists.side_effect = [False, True]
        self.settings.get.return_value = "/settings"
        
        result = resolve_file_path("/content", "file.txt", self.settings)
        
        self.assertEqual(result, "/settings/file.txt")

    @patch('os.path.isabs')
    @patch('os.path.exists')
    def test_resolve_file_path_fallback(self, mock_exists, mock_isabs):
        mock_isabs.return_value = False
        mock_exists.return_value = False
        self.settings.get.return_value = "/settings"
        
        result = resolve_file_path("/content", "file.txt", self.settings)
        
        self.assertEqual(result, "/content/file.txt")


if __name__ == '__main__':
    unittest.main() 