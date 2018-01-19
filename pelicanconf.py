# Basic settings {{{

OUTPUT_RETENTION = ['.git', ]

READERS = {'html': None}

PATH = 'content'

PLUGINS = []
PLUGIN_PATHS = []

SITENAME = 'JNRowe'
SITEURL = ''

STATIC_PATHS = ['.extras/', 'files']
EXTRA_PATH_METADATA = {
    '.extras/' + f: {'path': f}
    for f in ['.well-known/keybase.txt', 'google4ab4fc069ca34be6.html',
              'robots.txt']
}

# Play with toggling this
TYPOGRIFY = False

# }}}

# URL settings {{{

RELATIVE_URLS = True

AUTHOR_SAVE_AS = ''

# }}}

# Time and Date {{{

TIMEZONE = 'Europe/London'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

# }}}

# Metadata {{{

AUTHOR = 'James Rowe'

# }}}

# Pagination {{{

DEFAULT_PAGINATION = 10

# }}}

# Themes {{{

SITESUBTITLE = 'Ramblings of a tired mind'
GITHUB_URL = 'https://github.com/JNRowe/'

LINKS_WIDGET_NAME = 'Info'
LINKS = [
    ('Contact details', 'pages/contact.html'),
    ('Copyright information', 'pages/copyright.html'),
    ('Consulting services', 'pages/consult.html'),
    ('Projects', 'pages/projects.html'),
    ('Colophon', 'pages/colophon.html'),
]

SOCIAL = [
    ('GitHub', 'https://github.com/JNRowe/'),
]

# }}}
