"""
Pelican Citation Processor Plugin

Processes citations in articles using Pandoc's citeproc functionality.
Uses a global bibliography file instead of requiring individual bibliography files per article.
"""

import os
import subprocess
import tempfile
from pelican import signals
from pelican.generators import ArticlesGenerator


def process_citations(article_generator, content):
    """
    Process citations in article content using Pandoc.
    
    Args:
        article_generator: The Pelican article generator
        content: The article content object
    """
    if not hasattr(content, '_content'):
        return
    
    settings = article_generator.settings
    
    citation_style = getattr(settings, 'CITATION_STYLE', None)
    bibliography_file = getattr(settings, 'BIBLIOGRAPHY_FILE', '_bibliography.bib')
    
    if not citation_style or not bibliography_file:
        return
    
    bibliography_path = os.path.join(settings.get('PATH', ''), bibliography_file)
    if not os.path.exists(bibliography_path):
        return
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as temp_input:
            temp_input.write(content._content)
            temp_input_path = temp_input.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as temp_output:
            temp_output_path = temp_output.name
        
        pandoc_cmd = [
            'pandoc',
            '--from', 'html',
            '--to', 'html5',
            '--citeproc',
            '--csl', citation_style,
            '--bibliography', bibliography_path,
            '--output', temp_output_path,
            temp_input_path
        ]
        
        result = subprocess.run(
            pandoc_cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        with open(temp_output_path, 'r') as f:
            processed_content = f.read()
        
        content._content = processed_content
        
    except subprocess.CalledProcessError as e:
        print(f"Pandoc citation processing failed: {e}")
        print(f"Pandoc stderr: {e.stderr}")
    except Exception as e:
        print(f"Citation processing error: {e}")
    finally:
        if 'temp_input_path' in locals():
            try:
                os.unlink(temp_input_path)
            except OSError:
                pass
        if 'temp_output_path' in locals():
            try:
                os.unlink(temp_output_path)
            except OSError:
                pass


def register():
    """
    Register the plugin with Pelican.
    """
    signals.article_generator_write_article.connect(process_citations) 