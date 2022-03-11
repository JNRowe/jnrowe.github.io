.. post:: 2009-10-03
   :tags: GTK+, styling

Disabling cursor blinking in GTK+
=================================

Darren Roberts asks via the EADS Linux list:

    In pidgin_ how can I stop the cursor blinking?

Since we’ve had our Jabber_ server set up at the office there have been
countless questions about using pidgin_ to the various lists, and I feel the
answer that should often be given is:  Use something else.  There are plenty of
other clients available; empathy_ is installed on all our Solaris and Linux
boxes now, gossip_ may already be installed, emacs-jabber_ seems popular with
many of our emacs_ using developers, gajim_ comes recommended by a few users or
my favourite bitlbee_.  Now, with the rant out of the way we can go back to the
question at hand…

Cursor blinking is a severe annoyance for some people(not me, I patch apps to
add it), and disabling it for GTK+ applications is really quite simple.   If
you’re a GNOME_ user then the setting to change blinking is in the keyboard
properties dialog that can be found in the system menu.  If you’re using KDE_
you should edit :file:`~/.gtkrc-2.0-kde`.  If you’re using neither GNOME or KDE
you can add a directive to your :file:`~/.gtkrc-2.0`:

.. code-block:: cpp

    gtk-cursor-blink = 0

If it is just the blinking rate that bugs you, then you can give a different
value for ``gtk-cursor-blink``.  The value is given in milliseconds for the
blink frequency.

If you wish to only change the settings in pidgin you can edit
:file:`~/.purple/gtkrc-2.0` instead of your main :file:`~/.gtkrc-2.0`.

Bonus related tip
-----------------

If you’re really driven mad by the blinking cursor, and wish to disable it in
the console too then add the next little snippet to your shell’s startup file:

.. code-block:: bash

    echo -e '\033[?48c'

.. _pidgin: http://pidgin.im/
.. _Jabber: http://xmpp.org/
.. _empathy: http://live.gnome.org/Empathy
.. _gossip: http://developer.imendio.com/projects/gossip
.. _emacs-jabber: http://emacs-jabber.sourceforge.net/
.. _emacs: http://www.xemacs.org/
.. _gajim: http://www.gajim.org/
.. _bitlbee: http://www.bitlbee.org/
.. _GNOME: http://www.gnome.org/
.. _KDE: http://www.kde.org/

.. spelling::

    GTK
