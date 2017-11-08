:tags: gentoo, work, linux
:date: 2014-06-18

Dropping Gentoo
===============

We’ve been using Gentoo_ for shipped products since June 2005, and as
a development platform since September 2004.  A long time, an incredibly long
time in fact.

Today our final Gentoo using product shipped, with a single scheduled update
promised in Q3-2015.  It is kind of sad day, but we all knew that day was coming
and it takes only a little inside knowledge to know why.

.. _Gentoo: http://gentoo.org

.. note::

   A couple of people have rightly pointed out that I was a little harsh in
   this document, so I’ve pushed a :doc:`followup <dropping_gentoo_reflex>`.

Landscapes have changed
-----------------------

Back when we started using Gentoo it was clearly the best choice for what we
needed; a easily coercible base on which to construct our Linux devices.  There
actually weren’t a lot of viable choices back then.

Debian_, which many of us loved, felt like the only mainstream distribution we
could have used.  Unfortunately, it wasn’t available for the arches we needed.
It also didn’t package many of things we used at that point, but to be fair
there were :abbr:`ITPs (Intent to Package)` (were they called that back then?)
already floating about for most of them.

The “from source” options available then would, for all intents and purposes,
have meant taking on the support costs of the entire stack which nobody wanted
to commit to.  As it turns out that burden slowly crept up on us over the next
ten years anyway.

.. _Debian: http://debian.org

Take a left in 100 metres
-------------------------

Over the years we regrettably diverged heavily from upstream, almost to the
point that saying we use Gentoo almost feels like a lie.

Before our first product shipped we had already switched to maintaining the
essential toolchain packages like GCC and glibc ourselves.  I can’t recall the
specific reasons as I didn’t work on them, but I recall agreeing with them.

At some point we started using a custom package manager, initially just a new
drop-in resolver and eventually a completely independent package manager.
``portage`` was ferociously buggy in places and also appeared to be moribund, so
it seemed like the correct choice.  We never supported the full range of
features that Gentoo’s PMS_ now defines, but it made the support surface a lot
nicer.

There was a point where we seriously considered moving to a Conary_-based
infrastructure.  It did loads of the cool things we wanted to do and it mostly
fitted our workflow with its “Gentoo done right” feel.  Sadly, it has
a |CLA| which none of us could sign that practically guaranteed we would
eventually be in the same place we were with Gentoo.  May have been
a fortuitous roadblock in the end, as Conary never gained the traction it
once promised(perhaps in part because of that |CLA|?).

Had we waited another five months, there would have been another open source
package manager for Gentoo we could have easily switched to and hacked on.
There is perhaps a pattern here…

.. _conary: http://en.wikipedia.org/wiki/Conary_(package_manager)
.. _PMS: http://wiki.gentoo.org/wiki/Project:PMS

Upstreaming changes
-------------------

Of course, running a non-standard package manager and a thick layer of custom
packages at the bottom of the stack made contributing changes back upstream very
time consuming.  Many of us tried, but eventually most stopped.

Anyone who was running Gentoo in the mid-00’s will recall the giant wedge that
got in the way of reporting bugs, and sadly by the time it disappeared many of
us had lost interest.

If you had ran the gauntlet and lucked out with a bug in front of a developer,
there was a new barrier that many were irked by: lack of attribution.  It never
bothered me, but the number of developers who wouldn’t even reference a bug
report in the ChangeLog was huge.  That taught me a valuable personal lesson,
I always attribute a commit to the reporter even when I’ve significantly mangled
a patch to make it acceptable.

For a time, to ease the annoyance we used to play a game where we reported real
bugs with patches, but using silly data for ``emerge --info``.  It was
definitely fun while it lasted, but it didn’t solve the pain points.  Not
wanting to be associated with the bugs made people use pseudonyms, which also
removed the expectation of attribution too.

I kept trying to report trivial and cosmetic bugs - ones which didn’t require
a huge upfront investment - for some time, but they’d go unchanged for weeks or
months so I stopped doing that too

Looking around now there is an automatically generated list of bugs with patches
which we’ve fixed but haven’t upstreamed, and a few random entries from it look
like this:

.. sourcecode:: console

    $ wc -l ~/gentoo/to_push/jay.rst
    1157 /home/jay/gentoo/to_push/jay.rst
    $ wc -l ~/gentoo/to_push/mattias.rst
    2104 /home/jay/gentoo/to_push/mattias.rst
    $ wc -l ~/gentoo/to_push/chrisp.rst
    873 /home/jay/gentoo/to_push/chrisp.rst

That genuinely upsets me greatly.  The amount of potential duplicated effort
they represent is enormous, and I don’t even want to attempt to put a figure on
it.

Supporting upstream
-------------------

We’re entirely to blame.  We always planned on supporting upstream in whichever
way we could.  That fell down for instances beyond sending patches too.

The story that comes to mind is from a chance encounter at LinuxWorld back in
2005.  We had managed to gather a whole heap of really cool hardware to donate
to projects who were exhibiting on the day we attended, and it felt nice handing
out toys as a little “thank you” to the projects we depended on.

It wasn’t all roses though.  My manager went off to offer some ARM-based devices
to the Gentoo guys who were there, but was met with “tremendous rudeness” from
the person manning their desk at the time.  In hindsight people could have
predicted a similar outcome, and it was just an unlucky moment for him to walk
up.  That soured his enthusiasm no end, and it was the last time we managed to
score bags of toys to randomly give away to developers on any project.

If you were one of the people who received a Nokia tablet or ZipIt in the Hand
& Flower that evening, you now know the reason and perhaps you can even guess
who to thank.

A year or so later I watched a similar scenario play out at the Gentoo UK
conference with a potential sponsor and the same developer.  Evening beers were
met with other people telling stories about that same person, which was a shame
as it probably cost them a few good cash and infrastructure sponsors that day
alone.

Support costs
-------------

Over time we’ve come to support most of the tree that people refer to as
``gentoo-x86`` ourselves.  The toolchain changes we needed at the time
necessitated supporting a few packages further up the stack.  Our desire to trim
the tree of a few categories that were problematic, meant replacing a variety of
packages with then unavailable dependencies.

And there were many other examples too…

matchbox
''''''''

We packaged matchbox_ and its associated packages a long, long time before they
hit the official tree.  It was the first real pain point we had with packages
appearing in the tree after we had already been using them.

When they did eventually hit the tree we had to carry workarounds for years.  At
some point we stopped trying and just scrubbed the ebuilds that got in the way.

Python
''''''

The state of the Python packaging a few years ago made us take the jump to
replace or remove anything that packaged a Python module.  Initially very time
consuming, but it saved an enormous amount of grief.

I suspect we could move closer to upstream at this point, but the point is now
moot.

systemd
'''''''

We switched to ``systemd`` before the package was in upstream’s tree, and we
have had to keep supporting it to this day because of insurmountable packaging
differences.

In a few places that means taking on packages with a reverse dependency too,
where differences create issues.  And it clearly means taking on any package
that depends on ``openrc`` or Gentoo’s ``baselayout`` package.  Those packages
are becoming fewer and fewer by the day though, so that would have become
a non-issue.

X.org
'''''

We had been packaging x.org’s packages to work around some implementation
differences with upstream since the dawn of modular X.  Mostly just to do with
how dependencies were specified to start with, but they’re no longer even
remotely similar.

Luckily there isn’t a great deal of churn in the packages we care about for the
most part, so it never caused a huge time sink.

The end is nigh
---------------

At some point it began to feel like we were maintaining our own distribution
from end-to-end, and that wasn’t fun.  It also wasn’t what any of us needed to
do, and the time it was taking measurably ate in to *real* project time.

The decision to start weaning ourselves off of Gentoo was made back in the
summer of last year, and it has finally started to come in to effect.

The Times They Are a-Changing
-----------------------------

There are plenty of good alternatives out there now for building systems that
need to run on a variety of architectures.  Some binary, some source-based and
a few hybrid approaches.

The project I’m working on right now is using Debian ``testing``, and it appears
to be working out fine.  Some things still annoy me, like the time it takes to
patch and recreate a package.  It is a trivial thing with Gentoo, but requires
far too much work with Debian.  Perhaps we’ll improve the workflow enough as we
develop more experience.

We’ve also hit a good moment to use Debian because a whole heap of work has gone
in to making Debian easier to bootstrap, and it definitely shows.  When I find
out who has done all the magic to make that happen I’ll scribble down a note to
owe them some beers.

We’re also lucky in that we employ two Debian developers, one is practically
a funded full-time Debian developer.  They’re incredibly knowledgeable and it
makes working with Debian a lot easier, so thanks guys!

All told, things look good.  We’re still playing with some alternatives and as
yet no concrete decisions have been made, but I feel like we’re on the right
track for the next ten years.

So long Gentoo, and thanks for all fish!

