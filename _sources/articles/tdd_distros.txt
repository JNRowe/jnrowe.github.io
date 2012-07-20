:date: 2011-06-13

TDD distro development
======================

Using :abbr:`TDD (Test Driven Development)` for distribution development is a
hot topic in some of the more geeky circles I move in, and I'm very happy about
this.  Anything that increases the robustness of my desktop computer, my phone
or any other device I use is a great goal!

Why?
----

This answer should be obvious; more testing is good.  However, what about the
current system needs improving?

The first point is that commonly deployed distributions base their stabilisation
processes on the lack of *reported* bugs.  This implies that packages with a
minimal set of tests(or human testers in the common case) go through much less
testing than popular packages on their way to be marked as stable.  Of course,
this also implies that bugs in popular packages that will affect many users are
often discovered before a package is stabilised.

The second point is that a small set of bugs are actually regressions of
previously fixed bugs.  This, by itself, is a reason to look at alternatives.
Fixing the same bug more than once is an horrendous waste of developer
resources.

How?
----

We, the fine folks of AST's London office, already use a test-based
stabilisation policy in the preparation of our distribution images.  Adding
tests for new and bumped packages is something Leal Hétu and I have been
enforcing for the past few years.

Our packages and distribution images are used for the embedded devices we sell,
the desktops we develop on and the laptops we play on.  The methods we use vary
greatly, so I'm going to present the simple case of testing console applications
only.  It is the practise that is important, not the process.

The easiest method we use is via shelldoctest_, a module that implements a
:mod:`doctest` interface for testing shell commands.  The package provides a
user-level script for running shell sessions in Python docstrings.  A simple
example could be:

.. code-block:: python

    """
    $ echo test
    test
    $ echo fail
    liaf
    """

Running the previous file with ``shell-doctest test testdoc.py`` produces the
following output:

.. code-block:: pycon

    **********************************************************************
    File "testdoc.py", line 4, in testdoc
    Failed example:
        echo fail
    Expected:
        liaf
    Got:
        fail
    **********************************************************************
    1 items had failures:
       1 of   2 in testdoc
    ***Test Failed*** 1 failures.

Each time we bump a package, or add a completely new package, we also commit a
file containing a minimal series of tests that we consider important for the
package.  This allows us to almost instantly ascertain whether a future package
bump breaks functionality we require.

We also add a test *every single time* we fix a packaging bug, to make sure it
doesn't come up again.  A good example can be gleaned from a bug that was fixed
in our rails_ vim package.  Given the way the `vim scripts site`_ is organised
the files you want to download have awful download locations, so our ebuild for
the ``rails`` plugin contains the following snippet:

.. code-block:: bash

    DESCRIPTION="vim plugin: RoR - easy file navigation, enhanced syntax highlighting"
    HOMEPAGE="http://www.vim.org/scripts/script.php?script_id=1567"
    SRC_URI="http://www.vim.org/scripts/download_script.php?src_id=13800 -> ${P}.zip"

The ``SRC_URI`` declaration says we need to fetch the file from
``http://www.vim.org/scripts/download_script.php?src_id=13800`` and name it
locally as ``rails-4.3.zip``.  I'm sure you can guess what happened here,
someone saved a copy of the file locally for testing and forgot to update the
``src_id`` parameter correctly [#]_.  The result was an apparently new build
that installed an older package release.

When a fix for this bug was committed a test similar to the following snippet
was added to the ``rails`` test suite:

.. code-block:: python

    """
    $ grep -l "autoloaded_rails = '${PV}'" /usr/share/vim/vimfiles/autoload/rails.vim
    /usr/share/vim/vimfiles/autoload/rails.vim
    """

All this does is check the reported version is correct, and it clearly only took
a few seconds to write.  This is important, it shouldn't cost a lot to write a
test and this is especially true for the simplest task.

I use a similar technique for managing my public Gentoo overlay, jnrowe-misc_.
For example, the blockdiag_ ebuild is accompanied by a series of tests that are
run when bumping or stabilising the package, all of which are cribbed from my
actual ``blockdiag`` usage.  This massively reduces the time required to
evaluate a package at bump time.

Result?
-------

The time it takes to stabilise, or bump, a package may be massively reduced
while simultaneously increasing the robustness of the packages.  This is a huge
win, much bigger than we initially envisaged.

We still use time-based stabilisation, but in union with test-based
stabilisation.  It means that on the time-based stabilisation date we can
conveniently script the progression to stable including a final run of the test
suite.

I would, of course, prefer to see *any* tests upstreamed and where possible this
is already happening.  However, we're pragmatists and this means we often use
existing content as input for tests.  The use of existing input makes writing
the test faster and means each test exercises functionality we actually require,
but it also means we occasionally can't submit the data upstream owing to
licensing concerns.

Bonus
-----

I've used the upstream supported ``shelldoctest`` method for writing tests on
this page, but you can also easily specify them in `reST syntax`_ files too.
Doing this encourages you to write nicely formatted documentation to accompany
your tests.  You can also leverage your tests that are written in this way as
documentation using the excellent Sphinx_ tool.

The following script shows an extremely basic, yet fully functional, example of
how to combine the ``doctest`` module's :func:`~doctest.testfile` function with
``shelldoctest``:

.. code-block:: python

    #! /usr/bin/python -tt
    import doctest
    import sys

    import shelldoctest as sd

    sys.exit(doctest.testfile(sys.argv[1], module_relative=False,
                              extraglobs={"system_command": sd.system_command},
                              parser=sd.ShellDocTestParser())[0])

This script parses the first argument on the command line when it is run and
executes any ``shelldoctest`` blocks it finds.  It returns the count of failed
tests as its exit code, helpfully allowing you to execute a command with ``&&``
if all the tests pass.

We operate this way at AST, the above ``rails`` test would actually be part of
a ``reST`` formatted file as follows:

.. code-block:: rst

    Fix bug #xx, incorrect archive file::

        $ grep -l "autoloaded_rails = '${PV}'" /usr/share/vim/vimfiles/autoload/rails.vim
        /usr/share/vim/vimfiles/autoload/rails.vim

.. [#] Okay, it was me.  I'll confess.

.. _shelldoctest: http://pypi.python.org/pypi/shelldoctest/
.. _rails: http://www.vim.org/scripts/script.php?script_id=1567
.. _vim scripts site: http://www.vim.org/scripts/script.php?script_id=1567
.. _jnrowe-misc: https://github.com/JNRowe/jnrowe-misc
.. _blockdiag: http://pypi.python.org/pypi/blockdiag/
.. _reST syntax: http://docutils.sourceforge.net/docs/user/rst/
.. _Sphinx: http://sphinx.pocoo.org/
