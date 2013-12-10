import os


def add_tests(app):
    try:
        app.builder.templates.environment.tests['index'] = \
            lambda s: os.path.basename(s) == 'index'
    except AttributeError:
        # Ignore builders
        pass


def setup(app):
    """Add custom jinja tools."""
    app.connect('builder-inited', add_tests)
