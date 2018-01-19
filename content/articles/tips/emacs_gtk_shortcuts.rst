Proper keyboard shortcuts in GTK+
=================================

:summary: How to change keyboard shortcuts with GTK+
:tags: software, configs, GTK+, emacs
:date: 2007-03-05

If you’re used to the old style `GTK+`_ keyboard shortcuts, and find yourself
continually closing windows when you’re trying to delete a word (like me) then
add the following to your ``~/.gtkrc-2.0``::

    gtk-key-theme-name = "Emacs"

.. Note::
   This is for people using GTK+ apps, not GNOME.  If you wish to change
   bindings in GNOME you should use the control centre.

Using the above you can return to the old default format, but if you only want
to enable ``<C-w>`` and keep the other Windows-style shortcuts you can just
add::

    binding "gtk-emacs-text-entry"
    {
        bind "<ctrl>w" { "delete-from-cursor" (word-ends, -1) }
    }
    class "GtkEntry" binding "gtk-emacs-text-entry"
    class "GtkTextView" binding "gtk-emacs-text-entry"

If you use gtk-chtheme_ or gtk-theme-switch_ you should add custom options to
your ``~/.gtkrc.mine`` so it isn’t overwritten when you change themes.  See the
comments in your ``~/.gtkrc-2.0`` if you use either of these theme switchers.

.. figure:: /images/xfce4_keyboard.png
   :alt: XFce4 keyboard settings window

If you’re an XFce_ user you can select the Emacs keyboard shortcuts using the
keyboard settings dialog.

If you can’t change the settings for some reason, then you can still use
a shortcut to delete words.  The default setting, up to at least GTK+ v2.10.9,
is the finger-stretching ``<C-backspace>``.

And finally, if you manage to convince upstream that the default behaviour
should be the settings in the Emacs theme I’ll owe you a few beers!

.. _GTK+: http://www.gtk.org/
.. _gtk-chtheme: http://plasmasturm.org/code/gtk-chtheme/
.. _gtk-theme-switch: http://www.muhri.net/nav.php3?node=gts
.. _XFce: http://www.xfce.org/
