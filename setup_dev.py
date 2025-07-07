"""
Development setup script for Pelican Citation Processor plugin.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False


def check_pandoc():
    """Check if Pandoc is installed."""
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Pandoc is installed")
            return True
        else:
            print("✗ Pandoc is not working properly")
            return False
    except FileNotFoundError:
        print("✗ Pandoc is not installed")
        print("  Please install Pandoc from https://pandoc.org/installing.html")
        return False


def download_csl_file():
    """Download a sample CSL file."""
    csl_dir = Path("examples/content/_bib_styles")
    csl_dir.mkdir(parents=True, exist_ok=True)
    
    csl_file = csl_dir / "cambridge-university-press-author-date-cambridge-a.csl"
    
    if not csl_file.exists():
        print("Downloading sample CSL file...")
        url = "https://www.zotero.org/styles/cambridge-university-press-author-date-cambridge-a"
        if run_command(f"curl -o {csl_file} {url}", "Downloading CSL file"):
            print(f"✓ CSL file downloaded to {csl_file}")
        else:
            print("✗ Failed to download CSL file")
            return False
    else:
        print("✓ CSL file already exists")
    
    return True


def main():
    """Main setup function."""
    print("Setting up Pelican Citation Processor development environment...")
    print()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        return False
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check Pandoc
    if not check_pandoc():
        return False
    
    # Download CSL file
    if not download_csl_file():
        return False
    
    # Install development dependencies
    if run_command("pip install -e '.[dev]'", "Installing development dependencies"):
        print("✓ Development environment setup complete!")
        print()
        print("Next steps:")
        print("1. Run tests: pytest")
        print("2. Format code: black pelican/plugins/citation_processor/")
        print("3. Check style: flake8 pelican/plugins/citation_processor/")
        print("4. Test with example: cd examples && pelican content -s pelicanconf.py")
        return True
    else:
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 