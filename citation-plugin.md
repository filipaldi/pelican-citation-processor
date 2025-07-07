# Pelican Citation Plugin Assignment

## Objective
Create a Pelican plugin that processes citations using Pandoc directly, bypassing the limitations of the existing Pandoc Reader plugin.

## Problem
The [Pandoc Reader plugin](https://github.com/pelican-plugins/pandoc-reader) requires each article to have its own bibliography file (e.g., `my-post.md` needs `my-post.bib`). We need a global bibliography file approach.

## Solution
Create a plugin that:
1. Uses Pelican's default Markdown reader
2. Hooks into `article_generator_write_article` signal
3. Calls Pandoc directly with `--citeproc` for citation processing
4. Uses a global `_bibliography.bib` file

## Technical Requirements

### Plugin Structure
```
pelican-citation-processor/
├── pelican/plugins/citation_processor/
│   └── __init__.py
├── tests/
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

### Core Functionality
- Hook into Pelican's content processing pipeline
- Extract HTML content from articles
- Process citations using Pandoc subprocess call
- Replace content with citation-processed version
- Handle errors gracefully

### Pandoc Integration
```bash
pandoc --from html --to html5 --citeproc --csl=style.csl --bibliography=_bibliography.bib
```

### Configuration
```python
# pelicanconf.py
PLUGINS = ['citation_processor']
CITATION_STYLE = '_bib_styles/cambridge-university-press-author-date-cambridge-a.csl'
BIBLIOGRAPHY_FILE = '_bibliography.bib'
```

## Citation Format
Process `[@citation_key]` patterns in markdown content.

## Deliverables
1. Working plugin that processes citations
2. Tests for citation processing
3. Documentation for installation and configuration
4. Plugin ready for publication to PyPI

## References
- [Pelican Plugin Development Guide](https://docs.getpelican.com/en/latest/plugins.html)
- [Pandoc Citation Processing](https://pandoc.org/MANUAL.html#citations)
- [Existing Plugin Examples](https://github.com/pelican-plugins/)

## Success Criteria
- Citations like `[@DeepLearning2016]` are processed correctly
- Reference lists are generated for each article
- Global bibliography file works for all articles
- Plugin integrates seamlessly with existing Pelican workflow 