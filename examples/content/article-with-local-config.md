Title: Article with Local Citation Configuration
Date: 2024-01-16
Category: Research
Tags: citations, local-config, example
citation_style: _bib_styles/ieee.csl
bibliography_file: _local_bibliography.bib

# Article with Local Citation Configuration

This article demonstrates how to use local citation configuration that overrides the global settings. The article uses its own citation style and bibliography file.

## Local Configuration

This article specifies:
- `citation_style: _bib_styles/ieee.csl` - Uses IEEE citation style instead of the global style
- `bibliography_file: _local_bibliography.bib` - Uses a local bibliography file

## Example Citations

Here are some example citations that will be processed using the local configuration:

The field of machine learning has seen significant advances [@LocalML2023]. Recent developments in neural networks [@LocalNN2024] have shown promising results.

## Local Bibliography

The citations above reference entries in the local bibliography file `_local_bibliography.bib`, which is different from the global `_bibliography.bib` file.

## References

The references will be automatically generated using the local IEEE citation style. 