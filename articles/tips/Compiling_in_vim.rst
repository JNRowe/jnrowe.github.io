:date: 2009-09-24
:tags: vim

Compiling C source in vim
=========================

The fabulous Miss Biddulph asks via the EADS Linux list:

    Is there a way to make vim compile C files without a makefile?

A quick phone call later and we know that Laura wishes to emulate the make_’s
behaviour where calling ``make my_code`` without a ``Makefile`` will attempt to
build ``my_code`` from ``my_code.c``. vim_’s default ``:make`` command doesn’t
quite do the trick as it just calls ``make`` without any arguments.

vim allows us to set options for specific file types only using the ``:autocmd``
command, and this is the perfect time to use it.  We will set the value of
``makeprg``, which vim uses as the command to run with ``:make``, for all C and
C++ files.

.. code-block:: vim

    autocmd FileType c,cpp
        \ if glob("[Mm]akefile') == "" |
        \   let &makeprg="make %<" |
        \ endif

See :gist:`198024`

The ``%<`` in our ``makeprg`` definition refers to the current file with its
extension stripped.  We specifically only change the behaviour if no
``Makefile`` exists so that we don’t interfere with the normal usage of the
``:make`` command.

.. _make: http://www.gnu.org/software/make/make.html
.. _vim: http://www.vim.org
