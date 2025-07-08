"""
Example Pelican configuration for the Citation Processor plugin.
"""

# Basic Pelican settings
AUTHOR = 'Your Name'
SITENAME = 'My Academic Blog'
SITEURL = 'http://localhost:8000'

# Content settings
PATH = 'content'
OUTPUT_PATH = 'output'
DELETE_OUTPUT_DIRECTORY = True

# Theme settings
THEME = 'notmyidea'

# Plugin settings
PLUGINS = ['citation_processor']

# Citation Processor settings
CITATION_STYLE = '_bib_styles/cambridge-university-press-author-date-cambridge-a.csl'
BIBLIOGRAPHY_FILE = '_bibliography.bib'

# New Markdown citation processing settings
CITATION_PROCESSING_MODE = 'markdown'  # 'markdown', 'html', or 'auto'
CITATION_FALLBACK_TO_HTML = True      # Whether to fallback to HTML processing

# Debug settings (optional)
DEBUG = False  # Set to True for detailed processing information

# Feed settings
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

# Social widget
SOCIAL = (
    ('GitHub', 'https://github.com/yourusername'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True 