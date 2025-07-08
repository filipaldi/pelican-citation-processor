"""
Pytest configuration for the Pelican Citation Processor plugin tests.
"""

import pytest
from unittest.mock import Mock


@pytest.fixture
def article_generator():
    """Provide a mock article generator for tests."""
    generator = Mock()
    generator.settings = Mock()
    return generator


@pytest.fixture
def content():
    """Provide a mock content object for tests."""
    content = Mock()
    content._content = None
    return content


@pytest.fixture
def settings():
    """Provide a mock settings object for tests."""
    settings = Mock()
    settings.CITATION_STYLE = "style.csl"
    settings.BIBLIOGRAPHY_FILE = "_bibliography.bib"
    settings.CITATION_PROCESSING_MODE = "markdown"
    settings.CITATION_FALLBACK_TO_HTML = True
    settings.DEBUG = False
    settings.get.return_value = ""
    return settings 