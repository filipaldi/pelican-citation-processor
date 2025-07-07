# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial plugin implementation
- Support for global bibliography files
- Pandoc citeproc integration
- Configurable citation styles (CSL files)
- Comprehensive test suite
- Documentation and examples

### Features
- Hooks into Pelican's `article_generator_write_article` signal
- Processes citations in the format `[@citation_key]`
- Automatic reference list generation
- Error handling and graceful degradation
- Temporary file cleanup

### Technical Details
- Uses Pelican's default Markdown reader
- Calls Pandoc subprocess for citation processing
- Supports HTML input/output format
- Configurable via Pelican settings 