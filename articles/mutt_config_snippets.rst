.. post:: 2007-03-05
   :tags: software, configs, mutt

:command:`mutt` configuration snippets
======================================

.. highlight:: text

mutt_ is my favourite :abbr:`MUA (Mail User Agent)`, one of the few tools
I truly believe I couldn’t manage without.  It is also one of those tools,
along with vim_, which can end up sucking away all your free time to configure
it just how you want.

To get a quick idea of how many options you can configure with :command:`mutt`
run ``mutt -D | wc -l``, on my system with a heavily patched :command:`mutt`
1.5.13 it dumps just over 300 lines of output.  Of course, you shouldn’t need
to edit all of those settings though.

With the possibility of such large configuration files segregation is
important, and to aid that :command:`mutt` supports config file inclusion.  My
own :file:`~/.muttrc` takes advantage of this and consists of just the
following::

    source ~/.mutt/boolean.rc
    source ~/.mutt/colour.rc
    source ~/.mutt/format.rc
    source ~/.mutt/keys.rc
    source ~/.mutt/misc.rc
    source ~/.mutt/quad.rc
    source ~/.mutt/folders.rc
    source ~/.mutt/autoview.rc
    source ~/.mutt/gpg.rc
    source ~/.mutt/score.rc

    push <show-version>

The main config file simply includes all my other config files, and finally
displays the :command:`mutt` version number in the status line.  If you go down
this route, and I recommend it, just keep in mind that :command:`mutt`
processes the files in order so you can’t use variables that are defined in
later files.  The other thing to bear in mind while debugging is that
:command:`mutt` will be using the *last* set option, so if you try to set the
same variable in :file:`boolean.rc` and :file:`gpg.rc` :command:`mutt` will
override the value from :file:`boolean.rc` when it reads ``gpg.rc``.

The first config file to contain anything unusual is :file:`colour.rc`::

    # Match URLs in mail
    color body blue default "(finger|ftp|hg|http(|s)|news|tel)://[^ ]*"
    color body yellow black "mailto:[-a-z_0-9.]+@[-a-z_0-9.]+"
    # Match dates, both ISO-style and [YY]YY/MM/DD
    color body brightred black "\(19|20\)?[0-9][0-9][/-][01]?[0-9][/-][0123]?[0-9]"

    # Highlight qsf and SpamAssassin flagged mail
    color index brightred brightblack "~h '^X-Spam: YES'"
    color index brightmagenta brightblack "~h '^X-Spam-Status: Yes'"

    # ISBNs
    color body yellow default "[-0-9]{9,12}[0-9X]"

In :file:`keys.rc`::

    # Read mail using text-to-speech engine
    macro pager + "|festival --tts\r"

In :file:`misc.rc` you can find::

    # Fetch the spam rating as defined by qsf and SpamAssassin
    spam "X-Spam-Status: Yes, hits=([0-9]+.[0-9]*)" "Spam [%1]"
    spam "X-Spam-Rating: ([7-9][0-9]+)" "Spam [%1]"

You can then display the ratings in the :command:`mutt` index by using ``%H``
in your ``index_format`` string.  I personally choose to display the spam
rating instead of the date if it is found:

.. code-block:: text

    set index_format="%Z %2N %?H?%-12.12H&%D? %-16.16F  %s"

The important bit there is ``%?H?%-12.12H&%D?`` which displays twelve
characters of the spam value if it is found, or failing that the date.  The
reason we display exactly 12 characters of the spam value is so that the
columns line up correctly regardless of whether we display a date or a spam
value.  An example can be seen on the right featuring a few snippets from a ham
mailbox and my spam mailbox:

.. figure:: /.images/mutt_spam.png
   :alt: Spam field alignment in :command:`mutt`

The final, and perhaps most interesting, file is :file:`score.rc` where
I define all my manual scoring and some per-mail colouring policies.

The first thing we need to understand is that :command:`mutt` accumulates
scoring and colouring over its run time.  If you set a scoring policy of +20
for all mail from a certain domain each time you enter a folder 20 will be
added to the score of any mail from that domain.  If you leave :command:`mutt`
running for a long time this can easily end up skewing the displayed score.
The solution is simple, we tell :command:`mutt` to re-source the score file and
clear the settings every time we change folders::

    # Reread this file on every folder change
    folder-hook . source ~/.mutt/score.rc
    unscore *
    uncolor index *
    # Read our global colours again
    source ~/.mutt/colour.rc

Now we are free to setup our scoring policies without needing to worry about
whether a score will be calculated twice.  We can also set up per-folder
colouring much easier this way.

.. code-block:: text

    # Score mail to me, basically any mail which matches a value in
    # $alternates
    score ~p 40

    # Color UKFSN status mail, this way we can highlight the status
    # messages in the users mailing list and we don’t need to subscribe
    # to the specific status list.
    folder-hook UKFSN-users color index brightred black ~hX-Status-Mail:

    # Gentoo stuff
    # Color resolved Bugzilla bug mail
    folder-hook Gentoo-bugs color index brightred black ~hX-Resolved:
    # Watch for comments from Seemant in the bugstream
    folder-hook Gentoo-bugs 'color index brightyellow default ~fseemant@gentoo\.org'

:command:`mutt` allows you to search the entire message using the ``~b``
qualifier, but it can take an incredible amount of time to scan a large mailbox
if you use full body searches.  If you need to search in the mail body on
a routine basis it is better to add custom headers to your mail during
processing with your |MDA|, and then trigger rules based on those headers.

The Gentoo-bugs folder examples above use this method, because unfortunately
Bugzilla_ doesn’t give us anything else to work with.  I add a ``X-Resolved``
header if the mail contains :regexp:`^ \+Status|[^|]\+|RESOLVED$`.  And I set
the ``From`` header with the address taken from the first line that matches
:regexp:`^-{7} Comment #`, or :regexp:`^ {8}ReportedBy:`.  Those two |RegEx|
catch every Gentoo Bugzilla mail I’ve come across, except external bug state
changes which are left unchanged on purpose for easy highlighting.  I use
a non-public |MDA| system, so the actual rules aren’t very useful.

You can use any of the search attributes :command:`mutt` defines to set up
scores or colouring.  For example, you could set all mail older than 1 week to
a dull grey by matching on ``~d>1w`` as in:

.. code-block:: text

    folder-hook Gentoo-bugs 'color index brightblack default '~d>1w''

There are a lot of possibilities with :command:`mutt`, and there is a lot of
in-depth documentation included in the package.  If your distribution doesn’t
include it you can always head along to the mutt_ website and read it there.
Happy :command:`mutt`’ing.

.. |MDA| replace:: :abbr:`MDA (Mail Delivery Agent)`

.. _mutt: http://www.mutt.org/
.. _Bugzilla: http://www.bugzilla.org/
.. _vim: http://www.vim.org/
