import os


def add_tests(app):
    app.builder.templates.environment.tests['index'] = \
        lambda s: os.path.basename(s) == 'index'


def setup(app):
    """Add custom jinja tools."""
    app.connect('builder-inited', add_tests)
