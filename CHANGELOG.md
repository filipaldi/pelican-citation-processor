# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Support for processing citations directly from Markdown source files before HTML conversion
- Citations in Markdown format ([@citation-key]) are now properly formatted in the output
- Global and local bibliography and CSL file support
- Clean implementation and test suite, free of comments/docstrings

### Features
- Hooks into Pelican's `article_generator_write_article` signal
- Reads the original Markdown file for each article
- Runs Pandoc with citeproc, CSL, and bibliography file to generate HTML with formatted citations
- Replaces the article content with the processed HTML
- Error handling and debug logging
- Temporary file cleanup

### Technical Details
- Uses Pelican's default Markdown reader
- Calls Pandoc subprocess for citation processing
- Supports Markdown input/output format
- Configurable via Pelican settings 