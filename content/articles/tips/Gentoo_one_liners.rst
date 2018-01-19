Gentoo one liners
=================

:date: 2009-10-09
:tags: gentoo

On our Linux list at work the topic of Gentoo_ usage arose again today.
Originally, the topic was about interesting one liners used to maintain a Gentoo
system.  I found myself posting extended replies to some of the questions and
I’m reposting a few of those here.

    How do I get *just the list* of packages that are installed but not in
    ``world``?

The constraint here is packages that were installed with ``--oneshot``, or
manually removed from ``/var/lib/portage/world``, which means that they will no
longer be updated automatically.  I often use this for packages I’m just playing
with, and it appears lots of others do the same.  While the output of ``emerge
--pretend --depclean`` is all that is really needed, the question is how to get
a list of just the packages.

.. code-block:: console

    $ emerge --pretend --depclean
    <snipped heaps of output>
    gnome-base/orbit
        selected: 2.14.17
    protected: none
        omitted: none

    app-text/iso-codes
        selected: 3.8
    protected: none
        omitted: none

    dev-libs/dbus-glib
        selected: 0.76
    protected: none
        omitted: none

    sys-apps/dbus
        selected: 1.2.3-r1
    protected: none
        omitted: none

    >>> 'Selected' packages are slated for removal.
    >>> 'Protected' and 'omitted' packages will not be removed.

    Packages installed:   477
    Packages in world:    86
    Packages in system:   50
    Required packages:    348
    Number to remove:     129

The output we want can be easily matched with |RegEx|, and the bash_ ``alias``
below will list just the packages by piping the output through sed_.  We can
even use the one liner as input to a larger function if we only want to see
top-level packages; that is packages that aren’t listed as dependencies of other
packages::

    alias pkgclean="emerge ----pretend --depclean | sed -n '/^ [a-z]/s,^ ,,p' | sort"

    toppkgclean() {
        local depfiles=$(find /var/db/pkg/ -name RDEPEND -o -name PDEPEND)
        local cleanlist=$(pkgclean)
        for package in ${cleanlist}
        do
            LC_ALL=C grep -q ${package} ${depfiles} || echo ${package}
        done
    }

..

    Is it possible to use ``bash`` completion to complete package names for use
    in ``package.keywords``?

I actually wrote the following little function in reply to a user asking
a similar question in ``#gentoo`` on Freenode a couple of months ago:

.. code-block:: bash

    arch_unmask() {
        local s done
        if [[ -z $1 ]]
        then
            echo "${FUNCNAME} <category/package> [arch]"
            return 1
        fi
        for s in $(portageq envvar PORTDIR PORTDIR_OVERLAY)
        do
            if [[ -d $s/$1 ]]
            then
                echo $1 $2 >>/etc/portage/package.keywords/testing
                done=1
                break
            fi
        done
        if [[ -z "${done}" ]]
        then
            echo "Doesn't exist ‘$1’"
            return 1
        fi
    }
    complete -F _emerge arch_unmask

.. note::
   If you’re using our Gentoo boxes at the office the function will be much
   faster if you replace the call to ``portageq`` by ``/var/lib/repos/*``, as
   our package trees are always installed there.  The ``portageq`` call is
   mainly there for users who use ``/usr/portage`` and ``/usr/local/portage``,
   or other such monstrosities.

The final question I looked at was:

    Is there an easy way to clean all the old modules from ``/lib/modules``?

Assuming you are trying to remove all modules that don’t belong to the current
kernel this is very easy using ``bash``’s ``extglob`` support.  It may need to
be enabled in your session, you can test whether it is enabled with ``shopt
extglob``.

.. code-block:: console

    $ echo /lib/modules/*
    /lib/modules/2.6.31.1 /lib/modules/2.6.31.2-jr2 /lib/modules/2.6.31.3-mk1
    $ echo /lib/modules/!($(uname -r))
    /lib/modules/2.6.31.1 /lib/modules/2.6.31.2-jr2

The ``!($(uname -r))`` syntax tells bash to match all but ``2.6.31.3-mk1`` (the
output of ``uname -r`` on my system), there are plenty of other uses for
``extglob`` and the documentation_ has examples.

.. _Gentoo: http://www.gentoo.org/
.. _bash: http://cnswww.cns.cwru.edu/~chet/bash/bashtop.html
.. _sed: http://sed.sourceforge.net/
.. _documentation: http://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html#Pattern-Matching

.. include:: ../../../epilog.rst
