.. post:: 2009-10-07
   :tags: bts, devel

|BTS| as a task manager
=======================

.. highlight:: console

Tom Marshall asks over the cooler:

    What apps do you guys use to manage your todo list(s)?

I think this may be an incredibly personal thing but I prefer to use a |BTS|
for local task management, the idea of just adding random lines of text to
a file frankly baffles me.  I love the filtering, ordering and editing
capabilities I get from using a |BTS| for this.

Now, I’m not suggesting installing something complex and convoluted like
Bugzilla_ just for keeping track of your shopping lists or remembering to
charge the spare battery for your phone.  There are quite a few lightweight
systems available, ditz_ and `Bugs Everywhere`_ being two examples.  There is
also a :command:`ditz` inspired project, written in Python_, called pitz_ that
is in active development.  And fossil_ is pretty cool if you’re looking for
a standalone wiki, |BTS| and |VCS| in one.

.. note::
   If you’re a Gentoo_ user you can install :command:`ditz` using the ebuild
   from my overlay_.

I’m currently in the process of switching away from :abbr:`be (Bugs
Everywhere)`, but it can serve as an example quite well.  Unfortunately, there
are no releases currently being made so you will need to install a recent
version of :command:`bzr` to download it.  Don’t worry though you aren’t
restricted to :command:`bzr` to use it.

.. note::
   Colleagues from work can grab Dan’s ``be`` branch directly from our package
   repository, it doesn’t require :command:`bzr` and it fixes quite a few usage
   problems(it is also much faster).  Just remember that it has diverged
   massively from the upstream code, so you won’t be able to use it to work with
   bug databases created by the upstream project.

The following examples use an older version of :command:`be` that you can
download as a tarball_ and doesn’t require :command:`bzr`.

Setting :command:`be` up
------------------------

Before we use :command:`be` we must prepare it.  In the example that follows
we’re going to create a new directory under the control of git_, and tell
:command:`be` we wish to use it in there::

    $ mkdir be_test; cd be_test
    $ git init
    Initialized empty Git repository in /home/jay/Desktop/be_test/.git/
    $ be set-root
    Using git for revision control.
    Directory initialized.

Filing bugs
-----------

We can easily file new bugs, in the next snippet we can see two bugs being
filed.  Bugs are identified by a :abbr:`UUID (Universally Unique IDentifier)`,
and to operate on bugs we only need to use a unique prefix of the identifier as
can be seen below.

::

    $ be new "This is a test bug"
    Created bug with ID a09
    $ be assign a09
    $ git commit -m"Commit bug a09."
    $ be new "This is a second bug"
    Created bug with ID ec4
    $ be severity ec4 serious
    $ be comment ec4 "Comments are easy"
    $ git commit -m"Commit bug ec4."

We now have two bugs filed.  Bug ``a09`` is self-assigned, while ``ec4`` has yet
to be assigned.  As we didn’t set a severity level for ``a09`` it is set to the
default of ``minor``.  A comment was also made on bug ``ec4``, and if we hadn’t
specified the comment on the command line it would open our default editor to
add the comment.

Querying bugs
-------------

::

    $ be list
    ec4:os: This is a second bug
    a09:om: This is a test bug

The :command:`be list` output consists of three fields separated by colons and
they are: bug identifier, status and title.  The first character of the  status
field is an ``o`` telling us the bugs are marked as open, and the second
character is the severity indicator(where the ``s`` for bug ``ec4`` tells us it
is marked as serious).

You can also limit the bugs shown with :command:`be list` by specifying
severities with :option:`-v`.  Or bugs that are assigned to a certain user with
:option:`-a`, and you can use :option:`-m` to list bugs assigned to yourself.

When we wish to inspect individual bugs, to see there full status or comments,
we use the :command:`be show` command:

::

    $ be show a09
            ID : a0912cd6-1eae-490c-8e56-5f532242394b
    Short name : a09
        Severity : minor
        Status : open
        Assigned : James Rowe <jnrowe@gmail.com>
        Target :
        Creator : James Rowe <jnrowe@gmail.com>
        Created : Wed, 07 Oct 2009 14:11 (Wed, 07 Oct 2009 13:11:06 +0000)
    This is a test bug

    $ be show ec4
            ID : ec4438ca-a330-4345-b073-43c768f7e9b7
    Short name : ec4
        Severity : serious
        Status : open
        Assigned :
        Target :
        Creator : James Rowe <jnrowe@gmail.com>
        Created : Wed, 07 Oct 2009 14:11 (Wed, 07 Oct 2009 13:11:17 +0000)
    This is a second bug
    --------- Comment ---------
    Name: ec4:1
    From: James Rowe <jnrowe@gmail.com>
    Date: Wed, 07 Oct 2009 13:11:53 +0000

    Comments are easy

Editing bugs
------------

We can change the bug status with :command:`be status`, see the output from
:command:`be help status` for available values.

Once bugs are marked as fixed they no longer show up in the default
:command:`be list` output, but we can still view them with :command:`be show`
or by calling :command:`be list` with filtering options.

::

    $ be status ec4 fixed
    $ be list
    a09:om: This is a test bug
    $ be show ec4
            ID : ec4438ca-a330-4345-b073-43c768f7e9b7
    Short name : ec4
        Severity : serious
        Status : fixed
        Assigned :
        Target :
        Creator : James Rowe <jnrowe@gmail.com>
        Created : Wed, 07 Oct 2009 14:11 (Wed, 07 Oct 2009 13:11:17 +0000)
    This is a second bug
    --------- Comment ---------
    Name: ec4:1
    From: James Rowe <jnrowe@gmail.com>
    Date: Wed, 07 Oct 2009 13:11:53 +0000

    Comments are easy

Conclusions
-----------

That really is all it takes to use :command:`be`, and that is why I find
a |BTS| to be a nice solution for managing all kinds of random tasks.  I have
a Bugs Everywhere database in my home directory that over the past year has
stored just over 600 bugs from shopping lists to actual bugs with my
configurations files, and I’ve apparently managed to complete 95% of them!

Bonus material
--------------

One of the little tricks I like to do is override the :command:`cd` command to
automatically display the bug list when I enter a directory that contains a Bugs
Everywhere database, and it is very simple to do:

.. code-block:: bash

    cd() {
        local retval
        builtin cd "$@"
        retval=$?
        [[ ${retval} = 0 && -d .be ]] && be list
        return ${retval}
    }

It could be improved to take settings to filter the bug list or all manner of
other cool things, but that is why it has a “See gist #x” label next to it.
Feel free to post updates to the gist!

.. |BTS| replace:: :abbr:`BTS (Bug Tracking System)`

.. _Bugzilla: http://www.bugzilla.org
.. _ditz: http://ditz.rubyforge.org
.. _Bugs Everywhere: http://bugseverywhere.org/be/show/HomePage
.. _Python: http://www.python.org
.. _pitz: https://github.com/mw44118/pitz
.. _fossil: http://www.fossil-scm.org/index.html/doc/tip/www/index.wiki
.. _Gentoo: http://www.gentoo.org/
.. _overlay: https://github.com/JNRowe/jnrowe-misc/
.. _tarball: http://www.jnrowe.ukfsn.org/_static/be-0.0.193.tar.bz2
.. _git: http://www.git-scm.com/

.. spelling::

    standalone
