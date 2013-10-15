# coding=utf-8

import os
import sys

sys.path.extend([os.path.pardir, os.path.curdir, '/home/jay/Projects/feed'])

extensions = \
    ["sphinx.ext.%s" % ext for ext in ["intersphinx", ]] + \
    ["sphinxcontrib.%s" % ext for ext in []] + \
    ["ext.%s" % ext for ext in ["jinja", ]] + \
    ["%s" % ext for ext in ["feed", ]]


master_doc = 'index'
source_suffix = '.rst'

# General information about the project.
project = u'JNRowe'
copyright = u'2009-2013, James Rowe'

version = '0.1'
release = '0.1.0'

exclude_patterns = ['.build', 'README.rst']

pygments_style = 'murphy'
html_theme = 'agogo'

html_title = 'JNRowe'
html_logo = '.static/logo.png'
html_favicon = '.static/icon.ico'

html_static_path = ['.static', ]

intersphinx_mapping = {
    'python': ('http://docs.python.org/', os.getenv('SPHINX_PYTHON_OBJECTS')),
}
for proj in ['blanco', 'bleeter', 'bwatch', 'cupage', 'jnrowe-fixes',
             'pyisbn', 'upoints', 'versionah', 'vim-jnrowe']:
    # IDs must be alphanumeric
    proj_id = filter(lambda s: s.isalnum(), proj)
    intersphinx_mapping[proj_id] = ("http://jnrowe.github.com/%s/" % proj,
                                    "objects/%s.inv" % proj)

for proj in ['jnrowe-misc', ]:
    # IDs must be alphanumeric
    proj_id = filter(lambda s: s.isalnum(), proj) + 'docs'
    intersphinx_mapping[proj_id] = ("http://jnrowe.github.com/%s-docs/" % proj,
                                    "objects/%s.inv" % proj)
