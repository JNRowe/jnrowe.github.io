# Basic settings {{{

OUTPUT_RETENTION = ['.git', ]

READERS = {'html': None}

PATH = 'content'

PLUGINS = []
PLUGIN_PATHS = []

AUTHOR = 'James Rowe'
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

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
