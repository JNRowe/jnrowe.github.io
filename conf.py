# coding=utf-8

import os
import sys

import sphinx_rtd_theme

sys.path.extend([os.path.pardir, os.path.curdir, '/home/jay/Projects/feed'])

extensions = \
    ['sphinx.ext.%s' % ext for ext in ['extlinks', 'githubpages',
                                       'intersphinx', ]] + \
    ['sphinxcontrib.%s' % ext for ext in []] + \
    ['ext.%s' % ext for ext in ['jinja', ]] + \
    ['%s' % ext for ext in ['feed', ]]

# Only activate spelling, if it is installed.  It is not required in the
# general case and we don't have the granularity to describe this in a clean
# way
try:
    from sphinxcontrib import spelling  # NOQA
except ImportError:
    pass
else:
    extensions.append('sphinxcontrib.spelling')

master_doc = 'index'
source_suffix = '.rst'
html_copy_source = False

rst_epilog = """
.. |CLA| replace:: :abbr:`CLA (Contributor License Agreement)`
.. |DVCS| replace:: :abbr:`DVCS (Distributed Version Control System)`
.. |PyPI| replace:: :abbr:`PyPI (Python Package Index)`
.. |RegEx| replace:: :abbr:`RegEx (Regular Expression)`
.. |VCS| replace:: :abbr:`VCS (Version Control System)`
.. |XML| replace:: :abbr:`XML (Extensible Markup Language)`
"""

# General information about the project.
project = u'JNRowe'
copyright = u'2009-2017, James Rowe'

version = '0.1'
release = '0.1.0'

exclude_patterns = ['README.rst', '.build', 'draft']

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path(), ]

html_context = {'feed_link': True}
html_title = 'JNRowe'
html_favicon = '.static/icon.ico'

html_static_path = ['.static', ]

templates_path = ['.templates', ]

extlinks = {
    'pypi': ('https://pypi.python.org/pypi/%s', ''),
}

intersphinx_mapping = {
    'python': ('http://docs.python.org/', os.getenv('SPHINX_PYTHON_OBJECTS')),
}
for proj in ['blanco', 'bleeter', 'bwatch', 'cupage', 'jnrowe-fixes',
             'pyisbn', 'upoints', 'versionah', 'vim-jnrowe']:
    # IDs must be alphanumeric
    proj_id = filter(lambda s: s.isalnum(), proj)
    intersphinx_mapping[proj_id] = ('http://jnrowe.github.io/%s/' % proj,
                                    'objects/%s.inv' % proj)

for proj in ['jnrowe-misc', ]:
    # IDs must be alphanumeric
    proj_id = filter(lambda s: s.isalnum(), proj) + 'docs'
    intersphinx_mapping[proj_id] = ('http://jnrowe.github.io/%s-docs/' % proj,
                                    'objects/%s.inv' % proj)

spelling_lang = 'en_GB'
spelling_word_list_filename = 'wordlist.txt'
