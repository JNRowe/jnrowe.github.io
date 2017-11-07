#
"""conf - Sphinx configuration information."""

import os
import sys

from contextlib import suppress
from subprocess import CalledProcessError, PIPE, run

import sphinx_rtd_theme

sys.path.extend([os.path.curdir, os.path.pardir])

# General configuration {{{
extensions = \
    ['sphinx.ext.%s' % ext
     for ext in ['extlinks', 'githubpages', 'intersphinx', ]] + \
    ['sphinxcontrib.%s' % ext for ext in []] + \
    ['ext.%s' % ext for ext in ['jinja', ]] + \
    ['feed', ]

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

templates_path = ['.templates', ]

rst_epilog = """
.. |CLA| replace:: :abbr:`CLA (Contributor License Agreement)`
.. |DVCS| replace:: :abbr:`DVCS (Distributed Version Control System)`
.. |PyPI| replace:: :abbr:`PyPI (Python Package Index)`
.. |RegEx| replace:: :abbr:`RegEx (Regular Expression)`
.. |VCS| replace:: :abbr:`VCS (Version Control System)`
.. |XML| replace:: :abbr:`XML (Extensible Markup Language)`
"""

default_role = 'any'

needs_sphinx = '1.6'

nitpicky = True
# }}}

# Project information {{{
project = 'JNRowe'
copyright = '2009-2017  James Rowe'

version = '0.1'
release = '0.1.0'

trim_footnote_reference_space = True
# }}}

# Options for HTML output {{{
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path(), ]

html_title = 'JNRowe'

html_context = {'feed_link': True}
html_favicon = '.static/icon.ico'
html_static_path = ['.static', ]
html_extra_path = ['.well-known/', ]

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

# intersphinx extension settings {{{
intersphinx_mapping = {
    'python': ('http://docs.python.org/', os.getenv('SPHINX_PYTHON_OBJECTS')),
}
for proj in ['blanco', 'bleeter', 'bwatch', 'cupage', 'jnrowe-fixes',
             'pyisbn', 'upoints', 'versionah', 'vim-jnrowe']:
    # IDs must be alphanumeric
    proj_id = ''.join(filter(str.isalnum, proj))
    intersphinx_mapping[proj_id] = ('https://jnrowe.github.io/%s/' % proj,
                                    'objects/%s.inv' % proj)

for proj in ['jnrowe-misc', ]:
    # IDs must be alphanumeric
    proj_id = ''.join(filter(str.isalnum, proj)) + 'docs'
    intersphinx_mapping[proj_id] = ('https://jnrowe.github.io/%s-docs/' % proj,
                                    'objects/%s.inv' % proj)
# }}}

# spelling extension settings {{{
spelling_lang = 'en_GB'
spelling_word_list_filename = 'wordlist.txt'
# }}}
