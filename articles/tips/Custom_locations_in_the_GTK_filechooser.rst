:date: 2009-10-01
:tags: GTK+

Custom keybindings in the GTK+ file dialogs
===========================================

.. Yes, I know GTK+’s config isn’t a cpp, but the highlighting works…

.. highlight:: cpp

In :doc:`Fancy_awesome_theming` I included a screenshot that, by accident more
than design, spawned today’s tip.

.. image:: /.static/2009-10-01-gtkrc-mini.png
   :alt: gtkrc in vim screenshot
   :target: ../../_static/2009-09-28-awesome_theming.png
   :align: right

Laura Biddulph sent me a :abbr:`SMS (Short Message Service)` message that read:

    Thanks! I saw your :file:`gtkrc`, and now I have keybound faves in the file
    dialog.

The :file:`gtkrc` being referenced is my `GTK+`_ configuration file that could
be seen in the right hand vim_ window of the screenshot from that earlier post.
It was actually open in that screenshot because I was changing my GTK+ theme,
and not being a gnome_ user the simplest way to change it is via my
:file:`~/.gtkrc-2.0`.  And, if you’re using KDE_ and wish to the settings for
GTK+ applications you should edit :file:`~/.gtkrc-2.0-kde`.

So the question becomes, what were the options in that screenshot, and are there
any other cool and useful things you can do there?

::

    gtk-theme-name = "expose"
    gtk-icon-theme-name = "hicolor"
    gtk-key-theme-name = "Emacs"

    binding "some-shortcuts" {
        bind "<Alt>T" {
            "location-popup" ("/home/jay/urls")
        }
        bind "<Alt>M" {
            "location-popup" ("/var/lib/repo/jnrowe-misc")
        }
    }
    class "GtkFileChooserDefault" binding "some-shortcuts"

See :gist:`199268`

Ignoring the :command:`vim` modeline_ from the screenshot the first few
settings are basic theme related options.  ``gtk-theme-name`` and
``gtk-icon-theme-name`` set the style and icon groups for GTK+ apps
respectively.  ``gtk-key-theme-name`` sets the default keybindings for GTK+
apps.  By setting it to ``Emacs`` we have access to the “normal” keybindings we
expect if we use bash_ or other common Linux tools, such as :kbd:`C-w` to
delete the word under the cursor.  You can read more about
``gtk-key-theme-name`` in `an old posting of mine`_.

All of the settings above are configurable with a :abbr:`GUI (Graphical User
Interface)` if you use gnome or xfce_, but for those of who don’t use those
desktop environments editing the :file:`~/.gtkrc-2.0` is a reasonable solution.

.. image:: /.static/2009-10-01-GTK_filechooser-mini.png
   :alt: GTK file chooser screenshot
   :target: ../../_static/2009-10-01-GTK_filechooser.png
   :align: left

The “some-shortcuts” section is the interesting one for today, it is telling
GTK+ applications that we want to have our own extra keybindings available when
opening or saving files.  ``GTKFileChooser`` is the modern GTK+ file dialog, and
it already has a set of useful keybindings including:

+-----------------+--------------------------------------+
| Key             | Purpose                              |
+=================+======================================+
| :kbd:`M-<Home>` | Jump to your home directory          |
+-----------------+--------------------------------------+
| :kbd:`M-D`      | Jump to your ``~/Desktop`` directory |
+-----------------+--------------------------------------+
| :kbd:`M-<Up>`   | Go to current directory’s parent     |
+-----------------+--------------------------------------+
| :kbd:`C-L`      | Display the text location entry box  |
+-----------------+--------------------------------------+

We could actually use the file chooser’s bookmark feature, and access the
bookmarks with :kbd:`M-1` through :kbd:`M-9` and :kbd:`M-0` for bookmark number
ten from the dialog.  However, I find it more practical to be able to use
mnemonic names for favourite locations.  You could even use both if you have an
excellent memory and a lot of favourite locations!

If you wish to add your own bindings the format is hopefully quite
self-explanatory, just don’t forget to link your bindings to the correct class
or they will not work.

You can also change the default bindings by specifying them in the
configuration file, for example to use :kbd:`M-<left>` and :kbd:`M-<right>` to
skip backward and forward along the directory path::

    bind "<Alt>Left" {
        "up-folder" ()
    }
    bind "<Alt>Right" {
        "down-folder" ()
    }

See :gist:`199269`

Whether you find :kbd:`Up` and :kbd:`Down` or :kbd:`Left` and :kbd:`Right`
easier to remember depends on how you visualise the path, I personally prefer
the defaults in this instance but the choice is entirely yours.

If you decide to significantly modify the bindings you may even find it easier
to split the :file:`~/.gtkrc-2.0` in to chunks to make it easier to manage or
share, for this you can use the ``include`` directive.  An example would be:
``include "~/.gtk_bindings"``.

.. _GTK+: http://www.gtk.org/
.. _vim: http://www.vim.org/
.. _gnome: http://www.gnome.org/
.. _KDE: http://www.kde.org/
.. _modeline: http://vimdoc.sourceforge.net/htmldoc/options.html#modeline
.. _bash: http://cnswww.cns.cwru.edu/~chet/bash/bashtop.html
.. _an old posting of mine: http://www.jnrowe.ukfsn.org/articles/configs/gtk.html
.. _xfce: http://www.xfce.org/
