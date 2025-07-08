# Pelican Citation Processor

A Pelican plugin that processes citations in Markdown content using Pandoc, supporting global and local bibliography and CSL files.

## Features

- Processes citations from original Markdown source files before HTML conversion
- Supports global and local bibliography and CSL (citation style) files
- Citations in Markdown format ([@citation-key]) are properly formatted in the output
- Uses Pelican's default Markdown reader and integrates with the standard workflow
- Clean implementation and test suite, free of comments/docstrings

## Installation

### Prerequisites

- Python 3.8 or higher
- Pelican 4.0 or higher
- Pandoc with citeproc support
- Python-Markdown (for Pelican to process Markdown)

### Install Pandoc

**macOS:**
```bash
brew install pandoc
```

**Ubuntu/Debian:**
```bash
sudo apt-get install pandoc
```

**Windows:**
Download from [pandoc.org](https://pandoc.org/installing.html)

### Install the Plugin

```bash
pip install pelican-citation-processor
```

## Configuration

Add the plugin to your `pelicanconf.py`:

```python
PLUGINS = ['citation_processor']
CITATION_STYLE = '_bib_styles/cambridge-university-press-author-date-cambridge-a.csl'
BIBLIOGRAPHY_FILE = '_bibliography.bib'
```

You can override these settings in individual articles using metadata:

```markdown
Title: My Article
Date: 2024-01-15
citation_style: _bib_styles/ieee.csl
bibliography_file: _local_bibliography.bib
```

### Configuration Options

- `CITATION_STYLE`: Path to your CSL file (required)
- `BIBLIOGRAPHY_FILE`: Path to your global bibliography file (default: `_bibliography.bib`)
- `citation_style` (article metadata): Path to article-specific CSL file (overrides global)
- `bibliography_file` (article metadata): Path to article-specific bibliography file (overrides global)

## Usage

### 1. Create a Bibliography File

Create a global bibliography file (e.g., `_bibliography.bib`) in your content directory:

```bibtex
@book{DeepLearning2016,
  title={Deep Learning},
  author={Ian Goodfellow and Yoshua Bengio and Aaron Courville},
  year={2016},
  publisher={MIT Press}
}
```

### 2. Download a CSL File

Download a citation style from the [Zotero Style Repository](https://www.zotero.org/styles/):

```bash
mkdir -p _bib_styles
curl -o _bib_styles/cambridge-university-press-author-date-cambridge-a.csl \
  https://www.zotero.org/styles/cambridge-university-press-author-date-cambridge-a
```

### 3. Write Articles with Citations

Use the `[@citation_key]` format in your Markdown articles:

```markdown
# My Research Article

Recent advances in deep learning have revolutionized machine learning [@DeepLearning2016].

## References

The references will be automatically generated here.
```

### 4. Generate Your Site

```bash
pelican content
```

The plugin will process citations and generate reference lists for each article.

## How It Works

- Hooks into Pelican's `article_generator_write_article` signal
- Reads the original Markdown source file for each article
- Runs Pandoc with citeproc, CSL, and bibliography file to generate HTML with formatted citations
- Replaces the article content with the processed HTML

## Troubleshooting

- **Pandoc not found**: Ensure Pandoc is installed and available in your PATH
- **Bibliography file not found**: Check that `BIBLIOGRAPHY_FILE` points to an existing file
- **CSL file not found**: Verify that `CITATION_STYLE` points to a valid CSL file
- **Citations not processed**: Check that citation keys match entries in your bibliography file
- **Markdown not processed**: Ensure the `markdown` Python package is installed

## Development

- Clean codebase, no comments or docstrings
- Tests for Markdown citation processing, file path resolution, and error handling
- Run tests with:

```bash
pytest
```

## License

MIT License

## Acknowledgments

- [Pelican](https://blog.getpelican.com/) - The static site generator
- [Pandoc](https://pandoc.org/) - The universal document converter
- [Zotero](https://www.zotero.org/) - For citation styles and bibliography management 