.. post:: 2009-09-27
   :tags: bugzilla, mail

Bugzilla mail with real names
=============================

John Bateman rants on the EADS Linux list:

    Bugzilla_ annoys the hell out of me, why I can’t just choose “spoof
    :mailheader:`From` address” in bugspam is beyond me.  It makes filtering
    such a chore!!

I agree, and I’ve long since decided to fix the problem locally.  There are
unfortunately a couple of small prerequisites for using my method that you may
not have.  The first is that you need to be able to filter the content of the
mail easily, and the second is that you install
lbdb_.

:command:`lbdb` is a small tool designed for handling mail addresses in mutt_,
but it does not require you to use or even install :command:`mutt`.  What we
are going to do is use :command:`lbdb` and our own incoming mail to seed an
email-to-name database for our bugspam filtering.  We don’t even need to
configure :command:`lbdb` to use it for our purposes, although I do recommend
giving the package a try even if you use another mail client.

The :command:`lbdb` tool we want to use is :command:`lbdb-fetchaddr` which is
designed to generate an address search database for the :command:`lbdb`
``m_inmail`` method.  :command:`lbdb-fetchaddr` keeps a text database of all
the names, addresses and the last seen date of every address we pass through
it.  This allows our Bugzilla filter to work without us having to generate our
own email-to-name list assuming we receive mail from the bug commenter either
personally or on a list, at the cost of increased(albeit still negligible)
processing time.  I use maildrop_ to filter my mail and to tell the
:command:`maildrop` :abbr:`MDA (Mail Delivery Agent)` to update the
:command:`lbdb` database we add a simple rule to our :file:`~/.mailfilter`:

.. code-block:: text

    if ($SIZE < 32768)
        cc '| lbdb-fetchaddr -d "%FT%T%z"'

This tells :command:`maildrop` to pass all mails less than 32k in size through
:command:`lbdq-fetchaddr`, and we specify a nice |ISO|-8601 time format for
easy sorting and parsing should the need arise.  Now every mail that is
delivered with :command:`maildrop` and isn’t too large will have the sender
name and address recorded in :file:`~/.lbdb/m_inmail.list`.

Now on to the actual filtering script, which is written in Python_.  It only
uses modules from the Python standard library, so you don’t need to install
anything else.  I have tested it with 25000 unique entries in
:file:`~/.lbdb/m_inmail.list` and it still takes less than a thirtieth of
a second to run the filter on my desktop, so processing the database each time
we start up isn’t really an issue.  Also, the few small tests I’ve done suggest
that using “real” database engines doesn’t help and the only way to speed it up
significantly would be to write a small daemon to process the mail which seems
more than a little overkill to me.

.. code-block:: python

    #! /usr/bin/python3 -tt

    from csv import reader
    from email import message_from_file
    from os.path import expanduser
    from sys import stdin

    with open(expanduser('~/.lbdb/m_inmail.list')) as f:
        lbdb = reader(f, delimiter='\t')
    addresses = dict(rec[:2] for rec in lbdb)

    message = message_from_file(stdin)

    commenter = None
    for line in message.get_payload().splitlines():
        if line.endswith(' changed:'):
            commenter = line.split()[0]
            break
        elif line.startswith('------- Comment #'):
            commenter = line.split()[4]
            break
        elif line.startswith('        ReportedBy: '):
            commenter = line.split()[1]
            break

    # You could also filter the message content at this point if you wished.
    # The following, for example, would remove the “https” link and some of
    # the blank lines in Gentoo bugspam
    message.set_payload('\n'.join([message.get_payload().splitlines()[3], ]
                                + message.get_payload().splitlines()[6:]))

    if commenter in addresses:
        message.replace_header('from',
                               '"%s" <%s>' % (addresses[commenter], commenter))

    print(message.as_string())

The final addition to our :file:`~/.mailfilter` file enables our little Python
filter to process mail from Bugzilla and change its :mailheader:`From` address
if we have the information in the :file:`~/.lbdb/m_inmail.list` database.

.. code-block:: text

    if (/^From: bugzilla-daemon@/)
    {
        xfilter "~/.mailfilter.d/rewrite-name.py"
        to Mail/Gentoo-bugs
    }

And from now on, or at least once your ``m_inmail.list`` is sufficiently seeded,
your bugspam will have the commenter’s name and email address, making it much
easier to filter and process it in your favourite mail client.

.. _Bugzilla: http://www.bugzilla.org
.. _lbdb: http://www.spinnaker.de/lbdb/
.. _mutt: http://www.mutt.org
.. _maildrop: http://www.courier-mta.org/maildrop/
.. _Python: http://www.python.org/
