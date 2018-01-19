jnrowe-misc - The unsorted package overlay
==========================================

:date: 2014-06-30
:tags: jnrowe-misc, gentoo

..

    A collection of ``ebuild`` files with no overall theme.

:abbr:`TLDR (Too Long; Didn’t Read)`; For what it was jnrowe-misc_ served its
purpose well.

An island unto itself
---------------------

While it may come as a surprise to a few of the users(which would be most of
them) the overlay available on GitHub wasn’t the deliverable at any point in
time.  In fact, the often convoluted merge history in the repository probably
hinted at that quite a bit.

.. image:: /images/jnrowe-misc.png
   :alt: Tree view of ``jnrowe-misc`` history
   :width: 50%
   :align: right

``jnrowe-misc`` was always the combination of a few independently managed
repositories that I bundled up to make available for public consumption.
Eventually it ended up being mostly Python stuff, but that was because the
support burden of other packages was becoming more time consuming than I could
justify.

The *real* audience for the overlay, my co-workers, saw a different beast
entirely.  It used our keyword types and rules, it came bundled `with the tests
<{filename}../tdd_distros.rst>`_ I was unable to share and had a tighter
schedule for maintenance.

Still, I received a fair number of emails and live comments from users so I’ll
call that a success!

Upstreamed
----------

Sadly, very little was ever taken upstream(even less if you count the parts that
were credited).  This was entirely my fault.  I originally started exporting the
overlay because I was fed up with the new package process upstream, and it seemed
like the best way to deal with that for me.

I had hoped that some packages would be picked up, but didn’t actively push them
after the first few.

The overlay should have never touched packages that were available upstream,
but occasionally they overlapped when upstream added them.  The use of
``::shadow`` to workaround problems when new packages were added upstream
worked *really* well, and saved the few remaining hairs on my balding head.

Legacy
------

It looks like the majority of packages will continue to be maintained for the
foreseeable future, but regrettably it looks like the result will not be
available beyond a “open to all people who know where to look” organisation on
GitHub.

.. Hint: It’s the same place the other EADS overlays were mirrored to.

I’d like to change the new maintainer’s mind, but in all honesty I understand
their reasons.  I’ve stopped maintaining a lot of once public projects over the
past couple of years, and it is as refreshing as it is saddening.

.. _jnrowe-misc: https://github.com/JNRowe/jnrowe-misc
