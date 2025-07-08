#!/usr/bin/env python3
"""
Test runner for the Pelican Citation Processor plugin.
"""

import sys
import subprocess
import argparse


def run_tests(test_pattern=None, verbose=False, coverage=False):
    """Run the test suite."""
    cmd = ["python", "-m", "pytest"]
    
    if test_pattern:
        cmd.append(test_pattern)
    else:
        cmd.append("tests/")
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=pelican.plugins.citation_processor", "--cov-report=term-missing"])
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run tests for Pelican Citation Processor")
    parser.add_argument("--pattern", "-p", help="Test pattern to run (e.g., 'test_markdown')")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", "-c", action="store_true", help="Run with coverage")
    
    args = parser.parse_args()
    
    exit_code = run_tests(
        test_pattern=args.pattern,
        verbose=args.verbose,
        coverage=args.coverage
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main() 