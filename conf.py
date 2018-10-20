#
"""conf - Sphinx configuration information."""

import os
import sys

from contextlib import suppress
from subprocess import CalledProcessError, PIPE, run

import ablog
import alabaster

sys.path.extend([os.path.curdir, os.path.pardir])

# General configuration {{{
extensions = \
    ['sphinx.ext.%s' % ext
     for ext in ['extlinks', 'githubpages', 'intersphinx', ]] + \
    ['sphinxcontrib.%s' % ext for ext in []] + \
    ['ext.%s' % ext for ext in ['jinja', ]] + \
    ['ablog', 'alabaster']

# Only activate spelling if it is installed.  It is not required in the
# general case and we don’t have the granularity to describe this in a clean
# way
try:
    from sphinxcontrib import spelling  # NOQA: F401
except ImportError:
    pass
else:
    extensions.append('sphinxcontrib.spelling')

master_doc = 'index'

exclude_patterns = ['README.rst', '.build', 'draft']

templates_path = ['.templates', ablog.get_html_templates_path()]

rst_epilog = """
.. |CLA| replace:: :abbr:`CLA (Contributor License Agreement)`
.. |DVCS| replace:: :abbr:`DVCS (Distributed Version Control System)`
.. |HTML| replace:: :abbr:`HTML (HyperText Markup Language)`
.. |IRC| replace:: :abbr:`IRC (Internet Relay Chat)`
.. |ISO| replace:: :abbr:`ISO (International Organization for Standardization)`
.. |PyPI| replace:: :abbr:`PyPI (Python Package Index)`
.. |RegEx| replace:: :abbr:`RegEx (Regular Expression)`
.. |URL| replace:: :abbr:`URL (Uniform Resource Locator)`
.. |VCS| replace:: :abbr:`VCS (Version Control System)`
.. |XML| replace:: :abbr:`XML (Extensible Markup Language)`
"""

default_role = 'any'

needs_sphinx = '1.6'

nitpicky = True
# }}}

# Project information {{{
project = 'JNRowe'
author = 'James Rowe'
copyright = f'2009-2018  {author}'

version = '0.1'
release = '0.1.0'

pygments_style = 'monokai'

trim_footnote_reference_space = True
# }}}

# Options for HTML output {{{
html_theme = 'alabaster'
html_theme_options = {
    'pre_bg': '#272822',
    'font_family': '"Verdana", "Arial", sans-serif',
    'head_font_family': '"Times", "Calibri", serif',
    'logo': 'logo.png',
    'show_related': True,
}
html_theme_path = [alabaster.get_path(), ]
html_css_files = ['custom.css', ]

html_title = 'JNRowe'

html_baseurl = 'https://jnrowe.github.io/'
html_context = {'feed_link': True}
html_favicon = '.static/icon.ico'
html_static_path = ['.static', ]
html_extra_path = ['.extras', ]

with suppress(CalledProcessError):
    proc = run(['git', 'log', "--pretty=format:'%ad [%h]'", '--date=short',
                '-n1'],
               stdout=PIPE)
    html_last_updated_fmt = proc.stdout.decode()

html_copy_source = False

html_experimental_html5_writer = True
# }}}

# extlinks extension settings {{{
extlinks = {
    'gist': ('http://gist.github.com/%s', 'gist #'),
    'pypi': ('https://pypi.python.org/pypi/%s', ''),
}
# }}}

# ablog extension settings {{{
blog_title = project
blog_baseurl = html_baseurl

blog_authors = {
    'JNRowe': (author, html_baseurl),
}
blog_default_author = 'JNRowe'

post_date_format = '%F'
post_redirect_refresh = 1

html_sidebars = {
    '**': ['about.html', 'postcard.html', 'navigation.html',
           'recentposts.html', 'tagcloud.html', 'categories.html',
           'archives.html', 'searchbox.html'],
}

blog_feed_archives = True
blog_feed_fulltext = True
blog_feed_subtitle = 'Ramblings of a tired mind'
blog_feed_length = 15
# }}}

# intersphinx extension settings {{{
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/',
               os.getenv('SPHINX_PYTHON_OBJECTS')),
}
# }}}

# spelling extension settings {{{
spelling_lang = 'en_GB'
spelling_word_list_filename = 'wordlist.txt'
# }}}
