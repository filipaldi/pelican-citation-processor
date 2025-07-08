# Pelican Citation Processor

A Pelican plugin that processes citations using Pandoc with a global bibliography file, bypassing the limitations of the existing Pandoc Reader plugin.

## Problem

The [Pandoc Reader plugin](https://github.com/pelican-plugins/pandoc-reader) requires each article to have its own bibliography file (e.g., `my-post.md` needs `my-post.bib`). This plugin provides a global bibliography file approach.

## Features

- Uses Pelican's default Markdown reader
- Processes citations using Pandoc's citeproc functionality
- Supports global bibliography file for all articles
- Configurable citation styles (CSL files)
- Seamless integration with existing Pelican workflow

## Installation

### Prerequisites

- Python 3.8 or higher
- Pelican 4.0 or higher
- Pandoc with citeproc support

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

The plugin supports both global and local citation configuration. Local settings in individual articles override global settings.

### Global Configuration

Add the plugin to your `pelicanconf.py`:

```python
PLUGINS = ['citation_processor']

# Required: Path to your CSL (Citation Style Language) file
CITATION_STYLE = '_bib_styles/cambridge-university-press-author-date-cambridge-a.csl'

# Required: Path to your global bibliography file
BIBLIOGRAPHY_FILE = '_bibliography.bib'
```

### Local Configuration

You can override global settings for individual articles by adding metadata to the article's frontmatter:

```markdown
Title: My Article
Date: 2024-01-15
citation_style: _bib_styles/ieee.csl
bibliography_file: _local_bibliography.bib

# Article content...
```

### Configuration Options

**Global Settings (in `pelicanconf.py`):**
- `CITATION_STYLE`: Path to your CSL file (required)
- `BIBLIOGRAPHY_FILE`: Path to your global bibliography file (default: `_bibliography.bib`)

**Local Settings (in article metadata):**
- `citation_style`: Path to article-specific CSL file (overrides global)
- `bibliography_file`: Path to article-specific bibliography file (overrides global)

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

@article{Attention2017,
  title={Attention is All You Need},
  author={Ashish Vaswani and others},
  journal={Advances in Neural Information Processing Systems},
  volume={30},
  year={2017}
}
```

### 2. Download a CSL File

Download a citation style from the [Zotero Style Repository](https://www.zotero.org/styles/). For example:

```bash
mkdir -p _bib_styles
curl -o _bib_styles/cambridge-university-press-author-date-cambridge-a.csl \
  https://www.zotero.org/styles/cambridge-university-press-author-date-cambridge-a
```

### 3. Write Articles with Citations

Use the `[@citation_key]` format in your Markdown articles:

#### Global Configuration (Default)

```markdown
# My Research Article

Recent advances in deep learning have revolutionized machine learning [@DeepLearning2016]. 
The attention mechanism introduced by Vaswani et al. [@Attention2017] has been particularly influential.

## References

The references will be automatically generated here.
```

#### Local Configuration

For articles that need different citation styles or bibliography files:

```markdown
Title: My Specialized Article
Date: 2024-01-15
citation_style: _bib_styles/ieee.csl
bibliography_file: _specialized_bibliography.bib

# My Specialized Article

This article uses IEEE citation style and a specialized bibliography [@SpecializedRef2024].

## References

The references will be generated using the local IEEE style.
```

### 4. Generate Your Site

```bash
pelican content
```

The plugin will automatically process citations and generate reference lists for each article.

## How It Works

1. **Configuration Resolution**: The plugin resolves citation settings by checking local article metadata first, then falling back to global settings
2. **Content Processing**: The plugin hooks into Pelican's `article_generator_write_article` signal
3. **HTML Extraction**: Extracts the HTML content from each article
4. **Pandoc Processing**: Calls Pandoc with citeproc to process citations using the resolved configuration
5. **Content Replacement**: Replaces the article content with the processed version

### Configuration Resolution Order

1. **Local Settings**: Check article metadata for `citation_style` and `bibliography_file`
2. **Global Settings**: Fall back to global settings from `pelicanconf.py`
3. **Defaults**: Use default values if neither local nor global settings are provided

## Citation Format

The plugin processes citations in the format `[@citation_key]` where `citation_key` matches entries in your bibliography file.

## Troubleshooting

### Common Issues

1. **Pandoc not found**: Ensure Pandoc is installed and available in your PATH
2. **Bibliography file not found**: Check that `BIBLIOGRAPHY_FILE` points to an existing file
3. **CSL file not found**: Verify that `CITATION_STYLE` points to a valid CSL file
4. **Citations not processed**: Check that citation keys match entries in your bibliography file

### Debug Mode

Enable debug output in your Pelican settings:

```python
DEBUG = True
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/pelican-plugins/pelican-citation-processor.git
cd pelican-citation-processor
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black pelican/plugins/citation_processor/
flake8 pelican/plugins/citation_processor/
```

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Pelican](https://blog.getpelican.com/) - The static site generator
- [Pandoc](https://pandoc.org/) - The universal document converter
- [Zotero](https://www.zotero.org/) - For citation styles and bibliography management 