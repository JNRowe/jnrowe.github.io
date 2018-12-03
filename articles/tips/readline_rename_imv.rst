.. post:: 2018-10-26
   :tags: readline, imv, qmv, renameutils
   :excerpt: 2
   :image: 1

File renaming for the lazy
==========================

Over at HN in a `stolen topic`_:

   however, i miss one feature for which i'd use a filemanager: in-place file
   renaming. in most cases when i want to rename a file, i want to change
   a small part of it, and i don't want to have to retype the whole filename.

   i have yet to find a commandline utility (emacs doesn't count ;-) that
   offers that.

   -- em-bee

There a few interesting replies there, but I want to flesh out my replies
a little after the fact.

The new tool solution
---------------------

My initial reply was [#]_:

    If I’m understanding you correctly, then renameutils_’s ``imv`` is a great
    tool for this.  ``imv $filename`` pops you in to a readline_ enabled prompt
    to edit ``$filename``.  Given that it is ``readline`` you can even add
    extra options in your :file:`~/.inputrc` to add additional features to it,
    I have mappings for custom directory prefixes for example.

    It also comes with ``qmv``, which will pop open an editor for you to
    perform inplace edits on filenames.   Which is kinda like dired_ as an
    emacs_ comparison, at least if you squint an awful lot.

I recommend renameutils_ a lot.  I’ve given talks that have digressed in to
“why you should use ``qmv``”, I’ve mocked co-workers when I’ve spotted them
doing things ``imv`` would be a billion times better for, and it looks like
I even `pimped it`_ to distro folks in the past [#]_.

I sped across the usage in the HN comment, but there is some interesting
functionality hidden in there.  As stated, ``imv`` uses ``readline`` so you
have an enormous amount of `editing power`_ at your disposal, and it is all the
same stuff you have in your shell; ``<M-{b,f}>`` word jumps, ``<M-C-]>``
character searches, ``<C-t>`` to transpose typo fixes, ``<M-[count]>`` repeats,
and many more.

I also hinted at config file support.  :file:`~/.inputrc`, or whatever
:envvar:`$INPUTRC` points at, can be used to change the behaviour of all
``readline`` using tools.  Excitingly though, it can also be used to change the
behaviour of specific tools only.

For example, I often find myself writing throwaway scripts that I suddenly
decide I’ll want again in the future.  When that happens they move to
``~/.local/bin``, and I can do that with ``imv`` by tapping ``<C-v>`` at the
prompt.  This is really useful when I want to rename :file:`foo.sh` to
:file:`~/.local/bin/change_the_world.sh`.

.. code-block:: text

    $if imv
        set expand-tilde on
        C-v: '\C-a~/.local/bin\C-i'
    $endif

The above snippet might deserve a little explanation.  The ``<C-v>`` mapping
inputs ``<C-a>`` to move to the beginning of the line, the literal string
``~/.local/bin``, and finally the tab character(``<C-i>``)  to expand the tilde
for me.

Obviously, you can place whatever you want in there.  And if you take advantage
of the application guard as above, you can even override bindings that you
won’t find yourself using in ``imv`` without breaking your shell or other
tools.

.. figure:: /.images/borrow_your_laptop.png
    :alt: Borrow Your Laptop
    :scale: 50%
    :target: https://xkcd.com/1806/

    As always, xkcd_ has a pre-canned explanation for why you shouldn’t listen
    to me.  Image: `CC by-nc`_.

The old tool solution
---------------------

My other comment there was:

    If you’re a zsh_ user you can also use the other `zshexpn(1)`_ stuff too.
    Like ``mv file.ext{,(:r)}`` to perform ``mv file.ext file``, or ``:l`` to
    lowercase a filename, or any number of other sometimes useful(and often
    pointless things).  I’ve used ``:l`` a number of times, but ``:s`` for
    substitution is probably the most useful in general.

If you’re already using ``zsh`` (and you should be!), you have an enormously
powerful suite of functionality at your fingertips for every task including
simple renames.

I’ll show a few examples from a `quick interactive session`_ to hopefully make
the point.

.. code-block:: zsh

    $   # Real file names from my shared tips folder; co-workers look at
    $   # ``~JNRowe/public/tips`` for the actual content ;)
    $ echo xclip.rst{,(:r)}  # Remove extension
    xclip.rst xclip
    $ echo tile_in_60_seconds.rst{,(:u)}  # Change to all caps
    tile_in_60_seconds.rst TILE_IN_60_SECONDS.RST
    $ echo fzf_pkg_manager.rst{,(:u:A)}  # Change to all caps, and make path absolute
    fzf_pkg_manager.rst /home/jay/export/public/tips/FZF_PKG_MANAGER.RST
    $ echo dc.rst{,(:e)}  # Extract only extension
    dc.rst rst
    $ echo ogrmerge_layer_cake.rst{,(:A:h:h)}  # Extract parent directory from file
    ogrmerge_layer_cake.rst /home/jay/export/public
    $ echo xclip.rst{,(:s/clip/sel)}  # Apply substitution of “clip” to “sel”
    xclip.rst xsel.rst
    $ echo emacs_explore.rst{,(:s/e/X)}  # Apply subtitution of “e” to “X”
    emacs_explore.rst Xmacs_explore.rst
    $ echo emacs_explore.rst{,(:gs/e/X)}  # … add the g flag for global replace
    emacs_explore.rst Xmacs_XxplorX.rst

.. note::

    Order matters.  For example: in the ``(:u:A)`` example above we apply the
    uppercase filter first, and then convert to an absolute path.  If we’d
    reversed the modifiers the *entire* path would be converted to uppercase.

The modifiers are *hugely* powerful, and are definitely worth the effort to
learn in my opinion.  Combined with the ``readline`` emulation that ``zsh``
provides you can do some amazing things at the prompt.

They’re also available in non-interactive mode when writing scripts, and that
is probably when they’re at their most useful as you can apply them to other
constructs such as arrays as well.

.. tip::

    If you become accustomed to working with ``zsh`` and its advanced
    modifiers, then be sure to take a look at ``zmv`` which is bundled with
    ``zsh``.  It provides a nice interface to copying and moving files that
    makes heavy use of ``zsh``’s advanced features.  You may find it suits your
    way of working better than ``qmv`` for example.

Thoughts
--------

Small tools that do incredible things are *everywhere*, I clearly love
``renameutils`` but I’d also like to hear about those things you enjoy too.
Drop me a mail_, link me a blog post or stop me in the corridor to tell me
about them.

.. rubric:: Footnotes

.. [#] Lightly edited, because useful markup exists outside of HN.
.. [#] So long ago that *I* was surprised to find that out from a mairix_
       search to look for times when I’ve mentioned it.

.. _stolen topic: https://news.ycombinator.com/item?id=18290344
.. _renameutils: http://www.nongnu.org/renameutils/
.. _readline: http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
.. _dired: https://en.m.wikipedia.org/wiki/Dired
.. _emacs: https://www.gnu.org/software/emacs/
.. _pimped it: https://bugs.gentoo.org/show_bug.cgi?id=64479
.. _editing power: https://tiswww.cwru.edu/php/chet/readline/rluserman.html
.. _xkcd: https://xkcd.com/
.. _CC by-nc: http://creativecommons.org/licenses/by-nc/2.5/
.. _zsh: https://www.zsh.org/
.. _zshexpn(1): https://linux.die.net/man/1/zshexpn
.. _quick interactive session: https://linux.die.net/man/1/script
.. _mail: jnrowe@gmail.com
.. _mairix: http://www.rpcurnow.force9.co.uk/mairix/
