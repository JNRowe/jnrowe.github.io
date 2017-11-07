:date: 2009-09-23
:tags: mutt, styling

Theming mutt
============

Jeff, a work colleague, asks via IRC:

    Can I make mutt_ use a blue statusbar in X and red in console? A different
    colour would make it easier to read with a transparent urxvt.

mutt_ has access to environment variables when reading its configurations files,
so setting the theme based on term type is extremely easy.

First separate all your common settings in to one file, say
:file:`~/.mutt/colour_defaults.rc`.  Then add your per-term settings to a file
named ``~/.mutt/colour_$TERM.rc``.  Telling mutt to use the correct theme is
now as simple as adding the following to your :file:`~/.muttrc`:

.. Yes, I know mutt’s config isn’t a shell script, but the highlighting works…

.. code-block:: sh

    source ~/.mutt/colour_defaults.rc
    source ~/.mutt/colour_$TERM.rc

See :gist:`198012`

.. _mutt: http://www.mutt.org/
