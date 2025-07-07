"""
Development tasks for Pelican Citation Processor plugin.
"""

from invoke import task


@task
def format(ctx):
    """Format code using black."""
    ctx.run("black pelican/plugins/citation_processor/")


@task
def lint(ctx):
    """Run linting checks."""
    ctx.run("flake8 pelican/plugins/citation_processor/")


@task
def test(ctx):
    """Run tests."""
    ctx.run("pytest")


@task
def typecheck(ctx):
    """Run type checking."""
    ctx.run("mypy pelican/plugins/citation_processor/")


@task(format, lint, test, typecheck)
def check(ctx):
    """Run all checks."""
    pass


@task
def setup(ctx):
    """Setup development environment."""
    ctx.run("pip install -e '.[dev]'")


@task
def example(ctx):
    """Run example site generation."""
    with ctx.cd("examples"):
        ctx.run("pelican content -s pelicanconf.py") 