import sys

sys.path.append('.')

from pelicanconf import *


# Basic settings {{{

DELETE_OUTPUT_DIRECTORY = True

SITEURL = 'https://jnrowe.github.io'

RELATIVE_URLS = False

# }}}

# Feed settings {{{

FEED_DOMAIN = SITEURL

FEED_ALL_ATOM = 'updates.atom'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

FEED_MAX_ITEMS = 15

# }}}
