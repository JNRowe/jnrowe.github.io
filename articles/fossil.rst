:tags: ``fossil``, vcs, projects, development
:date: 2014-11-12

``fossil`` experiments
======================

For a variety of reasons we can no longer use GitHub at work for any project
which isn't Open Source.  And since that decision was thrust upon us we've been
playing with some alternatives for our workflow.  We'll probably end up choosing
one of the self hosted clones at some point, but it was decided early on that we
should evaluate a variety of options.

I was tasked with testing out fossil_ on a couple of small side projects, and
these are my *absolutely* biased personal findings.

Before I start I should add that while what I'm about to write probably sounds
harsh, I do like ``fossil`` the concept.  I like the single sqlite_ project
repository, I like the small-enough-to-grok-in-an-afternoon code base and I like
the idea of a totally reproducible project state including all metadata.

Testing ``fossil``
------------------

The good news is that testing ``fossil`` is a piece of cake.  It supports both
reading and writing ``git``'s fast-import_ format.  If you want to test it out
just dump an existing git_ repository(or `mercurial with an extension`_), and
feed it ``fossil import``.  If you later change your mind you can run ``fossil
export``.

Sadly supporting incremental two-way mirroring didn't work out for us, but
perhaps it will for simpler projects.  In the end I simply mirrored the
``fossil`` repository to ``git``, marked the ``git`` repositories as read-only
and forced contributors to work with ``fossil`` from the outset.

Packaging
---------

The ``fossil`` project sells itself on being a single file binary install, and
that probably works well for a subset of users.  We're not that in that subset
though, and ``fossil`` is more than a little annoying to wrangle in to our
environment.

The tarball ships without any *directly* usable documentation, so you end up
with either no system documentation or a collection of docs sprinkled with wiki
markup in :file:`/usr/share/doc`.

By default ``fossil`` builds in a manner which breaks most packaging standard
unfortunately.  If you're building packages you'll likely need to write an awful
lot of custom workarounds to get a compliant and usable package, see
``lst-pkgs/utils/dev/fossil`` build for the gory details of our hacks.

Uptake
------

I don't really want to hold this against ``fossil``, but it *is* important to
note that for all intents and purposes no one is familiar with it.  No upstream
projects we actively track use it, there isn't a single person who chooses to
use it on our site(which is why I had to handle the packaging) and expecting new
hires to have even heard of it is probably a stretch.

It wouldn't be such an issue if the choice was a ``git`` vs mercurial_ one,
where the few differences are mostly cosmetic.  ``fossil`` is a completely
different beast, and requires an enormous rethink in the way you handle version
control.

Ten years ago when people were on the whole still familiar with the CVS and
Subversion way of working that wouldn't have been such an issue, but times have
most definitely changed.

The vocabulary in the documentation is likely to be foreign to users of any
version control system, and the workflow examples in the documentation are
entirely foreign to how we have developed any project in at least the past
decade.

All-in-one solution
-------------------

One of the proclaimed benefits of using ``fossil`` is that it handles most
aspects of a project's :abbr:`ALM ()`; version control, issue tracking,
documentation(via a wiki), etc.  However, and this is only my opinion, it feels
like it does of all of these in a suboptimal manner.

Version control
'''''''''''''''

The version control feels quite nice for the most part, definitely usable but
a little annoying to work with if you're used to a modern :abbr:`DVCS
(Distributed Version Control System)` like we are.

That said it does feel like a *huge* step backwards when working with branches,
and you should set aside quite a lot of time for integration issues when you
have ``autosync`` disabled.  And I can't imagine a scenario where ``autosync``
could work for us, without rewriting our entire way of working or returning to
CVS-style mega commits and a manual patch stack layered on top.

If you read ``fossil``'s `Branching, Forking, Merging, and Tagging`_
documentation it appears that this is a design feature for the creators.

Issue tracker
'''''''''''''

The issue tracker feels like someone has tried to improve on Bugzilla_, without
taking a look at modern trackers.  It is definitely the weakest part of
``fossil`` in my opinion, using it is both a mental and eye-stabbing pain at the
same time.

Luckily you can rework a lot of it by fiddling around with the administration
settings exposed by ``fossil ui``.

This also exposes one of the best features of ``fossil``, you can create
a custom SQL script that configures the project(issue tracking, pretty theme,
etc) and just blast it in to the project's database.  Or you can create a custom
file that makes all your edits and pump it in with ``fossil config import``.

Wiki
''''

The wiki system is actually really good for what it does, but it has very few of
the features we use for our documentation.  I don't want to hold that against it
though, as it just a impedance mismatch.

The end result of the integrated components feels to me like you've chosen
a usable, but weak, component for every aspect of your project's :abbr:`ALM ()`.
The bits work well together, but none of them seem like an option you'd choose
on their own.

Interface
---------

The help output for new users is, in my opinion, really irritating.  The default
command message tells you to run ``fossil help`` or ``fossil help COMMAND``,
without providing the names of any of the common commands.  The ``fossil help``
output emulates a ``tsort`` filter of the command names, listing commands with
unique to ``fossil`` terminology and no short descriptions.  ``fossil help
--all`` feels like it should be more useful, but just creates a larger table of
commands with uncommon names and still no descriptions.

It makes very little sense to organise the help in this manner because as you
get used to the naming and non-standard option style you will need the help
less.  I've patched this for our packages, and if people like it I'll try to
push it upstream.

.. note::
   It turns out I won't be pushing the changes upstream.  They require
   a :abbr:`CLA (Contributor Licence Agreement)` that I can not sign in good
   faith, which is a shame.

The option handling *will* trip you up endlessly.  Just the little things like
being unable to chain options, and needing an endless stream of ``C-p M-5 M-b
<space>`` to add a space before a commit message for example.  Yes, I know some
people don't like standard ``getopt`` or GNU-style option parsing, but every
other tool you use has chosen it.

Some of the interface decisions are actively bad, for example there appears to
be no way to delegate password configuration to a trusted system service or even
``netrc``.  Specifying passwords in URLs on the command line is a **huge**
anti-pattern, and I just hope you don't have any multiseat systems if you're
using that method.

Speed
-----

On the whole ``fossil`` is fast, not ``git`` fast but fast nonetheless.  Commits
do take a disturbingly long time to complete for some reason, but most of the
other commands are fast enough.

Mangling a repository is actually a lot faster with ``fossil`` than any other
system I can think of, as you can just throw the power of SQL at it.  You can
find some sqlalchemy_ ORM definitions in :file:`/usr/share/doc/fossil/orm` in my
packages.

Conclusion
----------

I mentioned this in this first paragraph, but I don't see us moving to
``fossil``.  It is a nice system, but it just wouldn't work for us as is.

Part of me is tempted to attempt to fix the problems, but then we'd be left with
a system that is more obscure than ``fossil``.  If you read the `Fossil
Concepts`_ and `Frequently Asked Questions`_ documents you'll see that the most
significant problems for us are actually features for upstream, and that is
obviously fine but it does mean upstreaming changes would be impossible.

.. note::
   As noted above, it turns out they require a :abbr:`CLA (Contributor Licence
   Agreement)` which means we couldn't send changes upstream anyway.

That said I'm am planning on stealing some of the ideas that I really liked
about ``fossil`` for my own use.  ``fossil all``'s ability to run a command
against all repositories configured in :file:`~/.fossil` for example.

.. _fossil: http://www.fossil-scm.org/
.. _sqlite: http://sqlite.org/
.. _fast-import: http://git-scm.com/docs/git-fast-import
.. _mercurial with an extension: http://mercurial.selenic.com/wiki/FastImportExtension
.. _mercurial: http://mercurial.selenic.com/
.. _git: http://www.git-scm.com/
.. _branching, forking, merging, and tagging:
.. _bugzilla: http://www.bugzilla.org
.. _sqlalchemy: http://www.sqlalchemy.org/
.. _fossil concepts: http://fossil-scm.org/xfer/doc/tip/www/concepts.wiki
.. _frequently asked questions: http://www.fossil-scm.org/xfer/doc/tip/www/faq.wiki

