# Test Suite for Pelican Citation Processor

This directory contains the test suite for the Pelican Citation Processor plugin.

## Test Structure

The tests are organized into logical groups:

### `test_configuration.py`
Tests for configuration resolution functions:
- `resolve_citation_config()` - Citation style and bibliography file resolution
- `resolve_processing_config()` - Processing mode and fallback configuration

### `test_utils.py`
Tests for utility functions:
- `resolve_file_path()` - File path resolution logic

### `test_markdown_processing.py`
Tests for Markdown citation processing:
- `process_citations_markdown()` - Primary Markdown processing function
- Error handling and fallback mechanisms
- Debug logging functionality

### `test_html_processing.py`
Tests for HTML citation processing:
- `process_citations()` - Legacy HTML processing function
- `process_citations_html_fallback()` - HTML fallback processing
- Error handling and temporary file cleanup

### `test_citation_processor.py`
Legacy tests for backward compatibility.

## Running Tests

### Using pytest directly:
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_markdown_processing.py

# Run with verbose output
pytest -v tests/

# Run with coverage
pytest --cov=pelican.plugins.citation_processor tests/
```

### Using the test runner script:
```bash
# Run all tests
python run_tests.py

# Run specific test pattern
python run_tests.py --pattern test_markdown

# Run with verbose output
python run_tests.py --verbose

# Run with coverage
python run_tests.py --coverage
```

### Using unittest (legacy):
```bash
# Run specific test file
python -m unittest tests.test_configuration
python -m unittest tests.test_utils
python -m unittest tests.test_markdown_processing
python -m unittest tests.test_html_processing
```

## Test Configuration

The `conftest.py` file provides common fixtures:
- `article_generator` - Mock article generator
- `content` - Mock content object
- `settings` - Mock settings object

## Adding New Tests

When adding new tests:

1. **Choose the appropriate test file** based on functionality
2. **Use the provided fixtures** from `conftest.py`
3. **Follow the existing naming conventions**:
   - Test methods: `test_function_name_scenario()`
   - Test classes: `TestFunctionalityName`
4. **Add comprehensive docstrings** explaining what each test does
5. **Use appropriate mocking** to isolate the code under test

## Test Coverage

The test suite covers:
- ✅ Configuration resolution (global/local settings)
- ✅ File path resolution
- ✅ Markdown citation processing
- ✅ HTML citation processing
- ✅ Error handling and fallback mechanisms
- ✅ Debug logging
- ✅ Temporary file cleanup
- ✅ Backward compatibility

## Continuous Integration

Tests are automatically run in CI/CD pipelines to ensure:
- All functionality works as expected
- No regressions are introduced
- Code quality is maintained 