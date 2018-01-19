Sharing Xresources between systems
==================================

:date: 2009-10-05
:tags: X11, styling

In amongst the rants in our watercooler channel at work comes this question:

    So then, how do custom settings in ``Xresources`` work if you share your
    home directory between machines?

The question arises from a much larger topic concerning keeping your home
directory in a git_ repository.  The issue Carl is having is that he needs to
use different options on different machines and doesn’t relish the idea of
having to pull and rebase branches just to keep files in sync.  Of course, he
doesn’t have to do that and that is the point of this tip.

Basic conditionals
------------------

With great foresight the authors of xrdb_ decided that our ``Xresources`` file
should be preprocessed before it is used, the default preprocessor is ``cpp``.
On most of our systems at work, and likely most Linux systems in general,
``cpp`` is `GNU cpp`_.  Don’t worry about the size of the manual though, the
interesting features are easy to understand and use.  Let’s look at trimmed
example from my configuration file::

    #ifndef FIXED_FONT
        #define FIXED_FONT xft:Inconsolata:pixelsize=14:antialias=false
    #endif
    #ifndef BOLD_FIXED_FONT
        #define BOLD_FIXED_FONT FIXED_FONT:bold
    #endif

    urxvt.font: FIXED_FONT
    urxvt.boldFont: BOLD_FIXED_FONT

    irssi.font: FIXED_FONT

This small snippet sets a couple of default fonts that we can reference
throughout our resource file as ``FIXED_FONT`` and ``BOLD_FIXED_FONT``.  This
way we can easily change the value in one place and it trickles down to all our
programs.  Or we can define different options at runtime by specifying values to
``xrdb``, such as ``xrdb -DFIXED_FONT=xft:Monospace:pixelsize=10``.  And don’t
worry, ``cpp`` is smart enough to cope with the use ``=`` in our definition.

Per system conditionals
-----------------------

On one system I use Inconsolata_ is not installed, so the configuration above
wouldn’t work on it.  ``xrdb`` gives us a way around the problem though, it
defines a set of symbols we can use including one to test the system’s
``hostname``.  ``nebula``, the system that doesn’t have Inconsolata, does have
terminus_ and I can use that on there with a couple of small changes.

::

    #ifndef FIXED_FONT
        #ifdef SRVR_nebula
            #define FIXED_FONT xft:Terminus:pixelsize=14:antialias=false
        #else
            #define FIXED_FONT xft:Inconsolata:pixelsize=14:antialias=false
        #endif
    #endif

.. note::
   As we’re using X11_’s ``xrdb`` it is network aware, it defines
   ``SRVR_{name}`` for the ``X`` server name and ``CLNT_{name}`` for the client
   name.  Using these it is easy to configure systems where the server and
   clients are on different machines.

Conditionals for server options
-------------------------------

You can also change configured settings based on the extensions loaded in to the
server, for example to disable the screensaver in ``muxi`` if the :abbr:`DPMS
(Display Power Management Signalling)` extension is supported we’d test for
``EXT_DPMS``::

    #ifdef EXT_DPMS
        muxi.screensaver: false
    #endif

Testing your resource files
---------------------------

When you’re testing your own ``~/.Xresources`` file you can use the ``-n``
option with ``xrdb``, it tells ``xrdb`` to dump the settings as they would be
used instead of updating the resource database.  This makes it easy to check if
our conditional statements are working correctly without having to open and
close applications constantly.  You can also define and cancel symbol
definitions with the ``-D`` and ``-U`` options for ``xrdb``, this allows you to
test your modifications that rely on symbols that are normally exported by
``xrdb``.

Using a more featureful preprocessor
------------------------------------

You can also choose a different preprocessor if ``cpp`` isn’t up to your needs
by specifying a ``-cpp`` option to ``xrdb``.  The only caveat is that must
accept ``-D`` for defines, ``-U`` for symbol cancelling and ``-I`` for include
paths.  An example that does fit these restrictions is m4_, and it might be
a good choice if you wish to do mode advanced things in your configuration file
such as fancy filtering or the use of loops for defining colour tables.

.. _git: http://www.git-scm.com/
.. _xrdb: http://www.xfree86.org/current/xrdb.1.html
.. _GNU cpp: http://gcc.gnu.org/onlinedocs/gcc-4.4.1/cpp/
.. _Inconsolata: http://www.levien.com/type/myfonts/inconsolata.html
.. _terminus: http://www.is-vn.bg/hamster/
.. _X11: http://xorg.freedesktop.org/
.. _m4: http://www.gnu.org/software/m4/m4.html
