Importing gmail filters in mutt
===============================

:date: 2009-10-08
:tags: gmail, mutt

On our company’s Linux list Ryan Abbott is preparing to move to mutt_:

    I have some user filters setup in gmail_, and I’m wondering if there some
    way to make mutt use them?

Ryan has some filters set up for “premium” users who should be tagged in
a special way in the mail display so that they are much more noticeable.  Google
do support `exporting filters`_ now, and conveniently it is in well documented
format based on Atom_.  An example export, gleaned from Ryan but with personal
data removed, follows:

.. code-block:: xml

    <?xml version='1.0' encoding='UTF-8'?><feed xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
        <title>Priority filter</title>
        <id>tag:mail.google.com,2008:filters:1255006471524,31130756565258</id>
        <updated>2009-10-02T12:04:00Z</updated>
        <author>
            <name>Ryan Abbott</name>
            <email>rabbott@example.com</email>
            <uri>http://rabbott.example.com</uri>
        </author>
        <entry>
            <category term='filter'></category>
            <title>Joe Bloggs</title>
            <id>tag:mail.google.com,2008:filter:1255006471524</id>
            <updated>2009-10-01T09:23:11Z</updated>
            <content></content>
            <apps:property name='from' value='joe@example.com'/>
            <apps:property name='label' value='HiPri'/>
        </entry>
        <entry>
            <category term='filter'></category>
            <title>John Doe</title>
            <id>tag:mail.google.com,2008:filter:31130756565258</id>
            <updated>2009-09-23T14:59:45Z</updated>
            <content></content>
            <apps:property name='from' value='johndoe@example.com'/>
            <apps:property name='label' value='HiPri'/>
        </entry>
    </feed>


The exported filter is actually quite nice and we could just pull the email
addresses out with sed_:

.. code-block:: console

    $ sed -n "/name='from'/s,^.*value='\([^']\+\)'.*$,\1,p" filter.xml
    joe@example.com
    johndoe@example.com

.. warning::

    You shouldn’t parse |XML| with tools like ``sed`` or ``awk``.  There are
    plenty of |XML| processing tools available, and unlike ``sed`` they
    shouldn’t fail with files that contain namespaces or other |XML| features.
    Now I’ve said that, carry on using ``sed`` like I often do ;)

Once we have some way of getting at the email addresses we just need to add the
filters to ``mutt``.  For those of us who use ``mutt`` the normal approach to
prioritising in the gmail way is to use either colouring_ or scoring_:

.. code-block:: text

    color index brightgreen default ~fjoe@example.com
    score ~fjohndoe@example.com +20
    set index_format="%Z %2N %?H?%-16.12H&%D? %-16.16F  %s"

.. image:: /images/2009-10-08-mutt_screenshot.png
   :alt: colouring and scoring in mutt

The ``color`` example sets all mail from the fictitious Joe Bloggs in the mail
index to use a bright green foreground and the default background colour.  The
``score`` example adds another 20 points to mail from John Doe, we add it
instead of setting it directly is so that we can make use cumulative scoring.
We must make sure we include ``%N`` in our index_format_ setting to see the
scores in the mail index, the above ``index_format`` setting is the one
I currently use and it can be seen in the screenshot above.

I’m sure we’d prefer to automate the generation of the rules, and we can quickly
generate a list for ``mutt`` using our favourite |XML| processing tool.  Today
I’m using ruby_, because I know it is installed on Ryan’s system.  We’re going
to keep the identifier data from the Google export just in case we decide to
export our rules from ``mutt`` at some point in the future:

.. code-block:: ruby

    require 'rexml/document'
    doc = REXML::Document.new File.new(ARGV[0])

    doc.elements.each('feed/entry') do |entry|
        id = entry.elements["id"].text
        name = entry.elements["title"].text
        addy = entry.elements["apps:property"].attributes["value"]
        puts "# #{name}, #{id}"
        puts "score ~f#{addy} 20"
    end

Calling that script on the example data from above yields a small ``mutt``
configuration file that we can include in our mutt setup by adding ``source
<file_location>`` to our ``~/.muttrc``.

.. code-block:: text

    # Joe Bloggs, tag:mail.google.com,2008:filter:1255006471524
    score ~fjoe@example.com -20
    # John Doe, tag:mail.google.com,2008:filter:31130756565258
    score ~fjohndoe@example.com -20

A few years ago I posted some of tricks and tips I use for `configuring mutt`_,
which include some neat ways to colour and score mail on a per-folder basis.  It
may be worth taking a quick look at if you use folders to organise your mails.

.. _mutt: http://www.mutt.org/
.. _gmail: https://mail.google.com
.. _exporting filters: http://gmailblog.blogspot.com/2009/03/new-in-labs-filter-importexport.html
.. _Atom: http://www.atomenabled.org/
.. _sed: http://sed.sourceforge.net/
.. _colouring: http://www.mutt.org/doc/manual/manual-3.html#ss3.7
.. _scoring: http://www.mutt.org/doc/manual/manual-3.html#ss3.22
.. _index_format: http://www.mutt.org/doc/manual/manual-6.html#index_format
.. _ruby: http://www.ruby-lang.org/
.. _configuring mutt: http://www.jnrowe.ukfsn.org/articles/configs/mutt.html

.. include:: ../../../epilog.rst
