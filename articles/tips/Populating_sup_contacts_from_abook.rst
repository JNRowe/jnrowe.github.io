Populating sup contacts from abook
==================================

:date: 2010-03-23

A colleague from work, Adam Robertson, is switching to Sup_ from mutt_ and
wondering how to easily convert his contacts from abook_.  Given that it is my
constant pimping of ``sup`` that has convinced him to switch I feel obliged to
help with the conversion.

The first choice I may recommend is just to follow the wiki_ and use ``abook``
as a source for lbdb_.  I use a method similar to this quite successfully.

The second choice is to prime the contact list from ``abook`` with a little
Python_ script.  The ``sup`` contacts list uses a `very simple format`_ and
mangling the ``abook`` addressbook is possible in only a few lines of code:

.. code-block:: python

    #! /usr/bin/python -tt
    """Generate a sup contacts list from abook"""

    import configobj
    import os
    import sys

    def parse(file=None):
        if not file:
            file = os.path.expanduser("~/.abook/addressbook")
        conf = configobj.ConfigObj(file, list_values=False)
        for chunk in filter(lambda d: "nick" in d and "email" in d, conf.values()):
            print "%(nick)s: %(name)s" % chunk, \
                "<%s>" % chunk["email"].split(",")[0]

    if __name__ == "__main__":
        if len(sys.argv) > 1:
            if sys.argv[1] in ("-h", "--help"):
                print "%s [addressbook]" % sys.argv[0]
                sys.exit(255)
            addressbook = sys.argv[1]
        else:
            addressbook = None
        parse(addressbook)

`Fork this code <http://gist.github.com/340873>`__

The script requires the excellent configobj_ module.  You could also use the
ConfigParser_ module from the Python standard library, but ``configobj`` allows
my laziness to shine through with its simple dictionary-based access to the
parsed data.

The script opens either the named or default ``abook`` addressbook and fetches
any entries that contain both a ``nick`` and ``email`` section.  Those entries
are then output in format that ``sup`` accepts.  It includes only the primary
email address for the contact, as I tend to order contacts with multiple email
addresses in address preference order.

As I've mentioned before in :doc:`Making_a_nice_home` all these tasks should be
automated, and this one is no different.  To regenerate the contacts list when
the addressbook has been updated we can use make_:

.. code-block:: make

    .sup/contacts.txt: .abook/addressbook
        python sup_contacts.py $< >$@

`Fork this code <http://gist.github.com/340875>`__

Using this method allows us to continue using ``abook`` while having simple
access to our contacts from within ``sup``.  This is incredibly useful as it
means we can continue to use ``abook`` for other things too, see
:doc:`Kick_me_birthday_reminders`.

.. _Sup: http://sup.rubyforge.org/
.. _mutt: http://www.mutt.org/
.. _abook: http://abook.sourceforge.net/
.. _wiki: http://sup.rubyforge.org/wiki/wiki.pl?LbdbIntegration
.. _lbdb: http://www.spinnaker.de/lbdb/
.. _Python: http://www.python.org/
.. _very simple format: http://sup.rubyforge.org/wiki/wiki.pl?ContactsList
.. _configobj: http://www.voidspace.org.uk/python/configobj.html
.. _ConfigParser: http://docs.python.org/library/configparser.html
.. _make: http://www.gnu.org/software/make/make.html
