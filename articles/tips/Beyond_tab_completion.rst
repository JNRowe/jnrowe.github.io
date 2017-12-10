:date: 2009-09-30
:tags: bash, readline

Beyond simple tab completion
============================

Matt Taylor wrote on the EADS Linux list:

    ``wildmenu`` is to vim_ as ``$x`` is to bash_.  Define ``$x`` :)

The wildmenu_ option in :command:`vim` shows possible command line completions
above the command line, highlighting the currently selected completion option.
A follow up email later and Matt says:

    Basically, I want :command:`bash` to show me the completions and
    :kbd:`Tab`` to ``$key`` through them in the same way :command:`vim` does
    it.

The feature is surprisingly easy to achieve with :command:`bash`, and is
actually a feature of readline_ making it available to all software that uses
completion functionality from ``readline``.

The option we want is called menu-complete_, but it not bound to a key by
default.  You can enable ``menu-complete`` in all ``readline``-using
applications by editing your :file:`~/.inputrc` (or whatever :envvar:`$INPUTRC`
points to if it is set) or just for :command:`bash` if you do not wish to
change the behaviour of other applications.

To change the behaviour by editing the ``readline`` configuration file we would do
this:

.. code-block:: text

    "\C-a": menu-complete
    # Alternative version, enables menu-complete only for bash
    $if Bash
        "\C-a": menu-complete
    $endif

The above tells ``readline`` we wish to bind ``menu-complete`` to
:kbd:`Control-a`, I find that key combination quite comfortable as
:kbd:`Control-a` is easy to reach the my keyboard layout and is of little use
in any of the apps I use on a regular basis.  You must either re-read the
configuration file or restart the :command:`bash` session to enable this
binding.

To enable the key binding in :command:`bash` only we could also just edit the
appropriate :command:`bash` startup file:

.. code-block:: bash

    bind '"\C-a": menu-complete'

You must source the startup file or restart :command:`bash` to enable this
binding, alternatively you can just test the command in your current
:command:`bash` setting until you’re happy with the key combination.

In a follow up email on the list Matt asks if it is possible to make the
completion context aware, in much the same the bash-completion_ package does but
without having to write new completion scripts.  There are some other quite
useful completion modes available in :command:`bash`, I’ll describe a few
below.

:kbd:`M-!` tells :command:`bash` to complete command names be they actual
on-disk commands, functions or aliases. :kbd:`M-/` completes only filenames,
this can be very useful when ``bash-completion`` is refusing to tab complete
a filename for you.  :kbd:`C-$` implements variable name completion, this is
most useful when you’re looking to unset or re-set a variable.  Variable name
completion isn’t actually necessary if you have ``bash-completion`` installed
as it is smart enough to handle this for you in most cases.

And finally, there is a one more incredibly useful completion mode in
:command:`bash` and that is :kbd:`M-{`, it adds all possible completions to the
command line using the brace expansion syntax.  For example, if I type ``ls
~/Git/Local/<M-{>`` it completes to
``/home/jay/Git/Local/{Makefile,countless,dot-configs,haskvim,jrutils}``.
Using ``readline`` motion commands, especially word motions such as :kbd:`M-f`
and :kbd:`M-b` to jump forward and backward one word, I can easily apply
a command to a certain set of files in a directory.  Just don’t try it on
``/usr/bin`` unless you want to see how :command:`bash` handles massive command
lines!!

.. _vim: http://www.vim.org/
.. _bash: http://cnswww.cns.cwru.edu/~chet/bash/bashtop.html
.. _readline: http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
.. _menu-complete: http://cnswww.cns.cwru.edu/php/chet/readline/readline.html#IDX137
.. _wildmenu: http://vimdoc.sourceforge.net/htmldoc/options.html#'wildmenu'
.. _bash-completion: http://bash-completion.alioth.debian.org/
