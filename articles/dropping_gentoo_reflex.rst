:tags: gentoo, work, linux
:date: 2014-06-29

Dropping Gentoo reflex
======================

After hitting the publish button on :doc:`dropping_gentoo` a few friends
commented that I was either unnecessarily harsh about Gentoo or we wasted an
enormous amount of time on it.  It definitely was the former, and I feel
a touch ashamed for implying the latter.

I was writing my thoughts in the “project obituary” form that I’m used to, and
that is entirely about spotting the downsides to make sure they don’t reoccur.
And with that in mind I *was* being incredibly unfair to Gentoo, both the
project and by extension the people working on it.

There were many, many good points about Gentoo and I’ll nod towards a few now.

Speed
-----

No, no.  Not the “Oh my god, my KDEs are so fast” that many people fairly
associate with Gentoo users.  I’m talking about the basic package handling
tasks.

There are very few other distributions that can match Gentoo when it comes to
the speed of editing a package.  Or, for that matter, the speed of installation
if you share binary packages.

Almost the first thing you notice when switching to Debian or Fedora as a heavy
binary package user on Gentoo is just how slow package installation and removal
is.  Binary package installation on Gentoo feels on par with a distribution
like Slackware, and what passes for package management there is just choosing
the right argument to :command:`tar`’s :option:`-C` option.

Where Gentoo really excels though is in the speed of creating new packages or
editing existing packages.

Lets take a look at an example.  Say, for example, that you just found out that
``flask-dashed``’s  ``ebuild`` mistakenly installs a :file:`/usr/README` file.
We we can fix the problem with the following simple change and a call to
``repoman manifest``, the rest takes care of itself.

.. code-block:: diff

    diff --git i/flask-dashed-0.1b_p2.ebuild w/flask-dashed-0.1b_p2.ebuild
    index dd64877a387e..cf3e3cbf272b 100644
    --- i/flask-dashed-0.1b_p2.ebuild
    +++ w/flask-dashed-0.1b_p2.ebuild
    @@ -29,5 +29,6 @@ S="${WORKDIR}/${MY_P}"

     src_prepare() {
            distutils-r1_src_prepare
    +       sed -i /data_files/d setup.py || die "sed failed"
            rm -rf "${S}/tests"
    }

.. note::

   Of course, you should fix the package properly and send the fix upstream but
   this is just to prove a point.  Calling ``die`` with ``sed`` there isn’t
   recommended and is practically pointless, but it is the style upstream.

I have to mention a small downside here however, because very few people seem to
test ``portage``’s binary package support you’ll occasionally have to do some
leg work to fix problems.  This normally arises when you have an ``eclass``
change that needs to ripple through, or when a library breaks compatibility and
its ``ebuild`` hasn’t been bumped properly.

Almost every time that happens you can fix it with a quick loop in your shell
though.  A couple of such problems and solutions that I found in my shell
history can be seen below.

.. code-block:: sh

    # When you were stuck with packages that used python-distutils-ng, and you
    # needed to scrub packages because you changed Python version
    for s in $(portageq pkgdir)/*-*/*.tbz2; do
        qtbz2 -xO $s | qxpak -xO - ${${s##*/}/.tbz2}.ebuild | grep -q 'SUPPORT_PYTHON_ABIS' && echo $s
    done

    # When you were using packages that used python’s “-r1” eclasses and all
    # you could see is a flood of blockages in your update output
    for s in $(portageq pkgdir)/*-*/*.tbz2; do
        qtbz2 -xO $s | qxpak -xO - RDEPEND 2>/dev/null | grep -q "dev-python/python-exec" && echo $s
    done

Documentation
-------------

The excellent devmanual_ and the incredible `Package Manager Specification`_
made life so much easier.  The devmanual was both short enough to be used as
quick reference and complete enough that you could learn most of what you’d need
to know from it.  The unfortunately named PMS acted as the reference that
finally allowed us to switch from away from ``portage`` completely at the
office.

The PMS documented much of the nastiness that ``portage`` suffers from, and made
life in general a whole lot nicer when you were chasing bugs deep down the
rabbit hole.  And, let us be honest here it also stopped a little of the
fluidity that plagued ``portage`` too.

Some people argue that it acts as unnecessary stop motion but those people must
be forgetting what happened when behaviour changed randomly between ``portage``
versions.  PMS, and the EAPI process, also brought some much needed design and
stability to newer features.

All Gentoo users owe Ciaran McCreesh a few beers for all the hard work he put in
to those documents, especially in the early days.

.. _devmanual: http://devmanual.gentoo.org/
.. _Package Manager Specification: http://wiki.gentoo.org/wiki/Project:PMS

The personal touch
------------------

On a personal note I’ve met some awesome people over the years as a result of
using Gentoo.  Many of them at the old Gentoo UK conferences, which were always
fun.  More recently at LoFu’s annual summit which seems to have taken Gentoo
UK’s place with practically everyone you saw at Gentoo UK(minus the students),
and oddly about the same Gentoo to non-Gentoo ratio of talks too.

Two excellent people on our current team were recruited following the Gentoo UK
conference at UCL, and we met a spectacular contract hire at the one prior to
that as well.

I’ve even been lucky enough to have a few doors held open for me via people I’ve
met at Gentoo-themed or Gentoo-heavy events, and I suspect I’d be writing this
from a less happy place without them.

Wrapping up
-----------

It is true that you really can not always see the forest for trees.

Had recent events not clouded my vision I would have commented on the train
wreck that is ``webapp.eclass`` and ``app-admin/webapp-config`` in
:doc:`dropping_gentoo`.  It sucked tonnes and tonnes of time away until we
eventually just trashed any package that interacted with it and moved on.

That was so long ago that I had forgotten about it until a co-worker asked me
why I hadn’t mentioned it.  I suspect most of the other negative comments I made
will feel equally inconsequential when compared to the benefits Gentoo gave us
as time moves on.

Instead of making this rant even longer, I’ll take the time to reflect on the
fun memories.

