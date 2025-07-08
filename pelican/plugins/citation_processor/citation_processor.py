import os
import subprocess
import tempfile
from pelican import signals


def resolve_citation_config(article_generator, content):
    settings = article_generator.settings
    
    global_citation_style = getattr(settings, 'CITATION_STYLE', None)
    global_bibliography_file = getattr(settings, 'BIBLIOGRAPHY_FILE', '_bibliography.bib')
    
    local_citation_style = getattr(content, 'citation_style', None)
    local_bibliography_file = getattr(content, 'bibliography_file', None)
    
    citation_style = local_citation_style or global_citation_style
    bibliography_file = local_bibliography_file or global_bibliography_file
    
    return {
        'citation_style': citation_style,
        'bibliography_file': bibliography_file
    }


def resolve_file_path(base_path, file_path, settings):
    if os.path.isabs(file_path):
        return file_path
    
    content_path = os.path.join(base_path, file_path)
    if os.path.exists(content_path):
        return content_path
    
    settings_path = os.path.join(settings.get('PATH', ''), file_path)
    if os.path.exists(settings_path):
        return settings_path
    
    return content_path


def process_citations(article_generator, content):
    if not hasattr(content, '_content') or content._content is None:
        return
    
    settings = article_generator.settings
    citation_config = resolve_citation_config(article_generator, content)
    
    citation_style = citation_config['citation_style']
    bibliography_file = citation_config['bibliography_file']
    
    if not citation_style or not bibliography_file:
        return
    
    base_path = settings.get('PATH', '')
    bibliography_path = resolve_file_path(base_path, bibliography_file, settings)
    citation_style_path = resolve_file_path(base_path, citation_style, settings)
    
    if not os.path.exists(bibliography_path):
        if getattr(settings, 'DEBUG', False):
            print(f"Bibliography file not found: {bibliography_path}")
        return
    
    if not os.path.exists(citation_style_path):
        if getattr(settings, 'DEBUG', False):
            print(f"Citation style file not found: {citation_style_path}")
        return
    
    source_path = getattr(content, 'source_path', None)
    if not source_path or not os.path.exists(source_path):
        if getattr(settings, 'DEBUG', False):
            print(f"Source file not found: {source_path}")
        return
    
    try:
        with open(source_path, 'r') as f:
            original_content = f.read()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_input:
            temp_input.write(original_content)
            temp_input_path = temp_input.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as temp_output:
            temp_output_path = temp_output.name
        
        pandoc_cmd = [
            'pandoc',
            '--from', 'markdown',
            '--to', 'html5',
            '--citeproc',
            '--csl', citation_style_path,
            '--bibliography', bibliography_path,
            '--output', temp_output_path,
            temp_input_path
        ]
        
        if getattr(settings, 'DEBUG', False):
            print(f"Processing citations with command: {' '.join(pandoc_cmd)}")
        
        result = subprocess.run(
            pandoc_cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        with open(temp_output_path, 'r') as f:
            processed_content = f.read()
        
        content._content = processed_content
        
        if getattr(settings, 'DEBUG', False):
            print(f"Successfully processed citations for {source_path}")
        
    except subprocess.CalledProcessError as e:
        if getattr(settings, 'DEBUG', False):
            print(f"Pandoc citation processing failed: {e}")
            print(f"Pandoc stderr: {e.stderr}")
    except Exception as e:
        if getattr(settings, 'DEBUG', False):
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
    signals.article_generator_write_article.connect(process_citations) 