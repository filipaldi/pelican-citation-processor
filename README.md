# Pelican Citation Processor

A Pelican plugin that processes citations using Pandoc with a global bibliography file, bypassing the limitations of the existing Pandoc Reader plugin.

## Overview

This repository contains a Pelican plugin that enables citation processing in your static site. Unlike the existing Pandoc Reader plugin that requires individual bibliography files per article, this plugin uses a global bibliography file approach.

## Quick Start

```bash
# Install the plugin
pip install pelican-citation-processor

# Add to your pelicanconf.py
PLUGINS = ['citation_processor']
CITATION_STYLE = '_bib_styles/your-style.csl'
BIBLIOGRAPHY_FILE = '_bibliography.bib'
```

## Features

- ✅ Global bibliography file for all articles
- ✅ Pandoc citeproc integration
- ✅ Configurable citation styles (CSL files)
- ✅ Seamless Pelican integration
- ✅ Comprehensive test suite
- ✅ MIT License

## Documentation

For detailed documentation, examples, and configuration options, see the [main plugin directory](pelican-citation-processor/).

## Development

```bash
# Clone the repository
git clone https://github.com/pelican-plugins/pelican-citation-processor.git
cd pelican-citation-processor

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black pelican/plugins/citation_processor/
```

## Contributing

Contributions are welcome! Please see our [Contributing Guide](pelican-citation-processor/CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](pelican-citation-processor/LICENSE) file for details.

## Acknowledgments

- [Pelican](https://blog.getpelican.com/) - The static site generator
- [Pandoc](https://pandoc.org/) - The universal document converter
<<<<<<< HEAD
- [Zotero](https://www.zotero.org/) - For citation styles and bibliography management
=======
- [Zotero](https://www.zotero.org/) - For citation styles and bibliography management
>>>>>>> 8e1698d (Improve root README and add .gitignore for assignment file)
