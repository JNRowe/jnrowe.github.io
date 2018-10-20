.. post:: 2014-09-03
   :tags: oss, burnout, life

Open Source and enjoyment
=========================

A few years ago I burned out on Open Source projects, to the point that it was
close to impacting other parts of my life.  I have only myself to blame as
I didn’t manage to distance myself at all well.  Distancing yourself is not easy
to do when your fun hobby for relaxation is the thing that is working against
you.

There were a variety of incredibly minor issues that piled up Jenga-style.  Then
to carry the weak analogy forward, it toppled over in a split second like Jenga
in a rubber dingy on the rolling seas with a fumbling drunken friend wearing
a blindfold.

I’ve decided to write down a few of the things that were happening, both as an
act of catharsis and to help me spot the problems in future.  Perhaps it will
help others who are experiencing the same thing but haven’t quite spotted the
catalysts yet.

Dealing with needy users
------------------------

Some users seem to feel a disproportionate amount of “you work for me”,
seemingly more so than happens with actual paying customers on other projects
which strikes me as strange.  They’ll bug you endlessly in emails, in the issue
tracker, on |IRC| and in real life if you end up at the same conference.  You
*need* to stop this before it takes hold.  It helps if you can be polite, but
if not just stop it anyway.  It is for *your* welfare, so just do it.

I actually found myself burning the wrong people towards the peak of that
imaginary Jenga tower.  You need to make a concerted effort to figure out which
people are delivering the seemingly endless grief or perhaps just relentless
bikeshedding_, and stop them.  It is all too easy to accidentally become
annoyed at well meaning useful contributors when you’ve been trawling through
a heap of useless meta-discussion about a change nobody is making.

On one *library* project I worked on there was a user who didn’t read the
documentation, couldn’t use the language enough to write tests, yet still
endlessly sucked up support time by opening awful issues and sending pointless
emails wishing to discuss changes they might make.  I kind of hesitate to say
awful issues, but - for example - if you can’t write a two line assertion in
a language you’re not in the target audience for a library in the first place.

Those people aren’t even adding value in pointing out deficiencies in
documentation, because they’re not a target user.  It would be like me writing
to JCB_ telling them they must document why they use round knobs on the digger
I saw someone else using.  So try spot it early, and put a stop to it.

..
    If you want to know why :pypi:`github2` never spawned |API| v3 support, now
    you do.  To some extent it was probably a good thing as the replacement was
    a clean reimplementation, without the baggage that supporting both |API|
    versions would have required.  In other ways it was bad as we could have
    used the momemtum to push a single library, instead of the tonnes of half
    finished skeletons we seem to have now.

I suspect a big part of the issue here is cost.  I’m sure if there was even
a single penny cost to opening issues or sending a mail it would do wonders for
communication in general.  I suspect that would remain true even if you
reimbursed that penny immediately.

The simple answer
'''''''''''''''''

I figured out how to work with this entirely by accident.  Politely offer
answers that move them away from you.  It is by far the easiest solution.

In one instance I suggested alternative packages to an expensive user, with the
hope they’d quietly move on.  Which is evil really, as what you’re really doing
is dreaming that they’ll move on to bother a developer who isn’t you.

On another occasion I stole an idea from a friend and said “Sorry, I can’t
figure out how to implement this.  Open a pull request, and I’ll merge it!” to
another.  It worked well, because it stopped the direction-less discussion and
was never going to be followed up with a patch later.

Dealing with unreasonable requests
----------------------------------

I used to get quite annoyed when I received an impolite or unreasonable request
on an Open Source project, nowadays I tend to just respond with pre-canned
answers for most of them.  If you can cut the time it takes to respond to them,
you’ll obviously spend far less time thinking about them.

The typical one that springs to mind is a user complaining that you’ve not
licensed your |GPL| code in a way which allows them to use it without
contributing anything in return.  I choose reciprocating licences where I can,
because frankly that may be the only value you provide *me* as a user.  I get
that some people need to use their Open Source projects as a way to improve
their CV or build a presence, but for many of us it is just for fun and
reciprocation.

..
    My normal response now is a cuddlier version of this: “If you don’t want to
    reciprocate, that is fine by me.  But you need to write your own code, I’m
    not working for you.  I’m offering to work *with* you.”

Another example that I recall, but wish I didn’t, was a user *telling* me to
recompress a tarball on |PyPI| because their infrastructure couldn’t support
:command:`bzip2`.  Seems reasonable enough, but it came wrapped in a tirade of
abuse.  I ignored the abuse, uploaded another tarball and then received another
abusive email in return the next day.  That was a long time ago, far before the
burnout started to creep in so I just addressed the actual issue and moved on.

The answer
''''''''''

I had forgotten about that whole previous story until at Europython_ a friend
was telling me about someone who was banned from a number of events, hell-banned
on various mailing lists and on forced lockout on Stack Overflow for poisonous
behaviour.  I started to tell my story as an example of strange abusive
behaviour, and it turned out to be the same guy.

The point is these people can be everywhere so just don’t let them get to you.
I realise that is both obvious and feels hard to do, but it is quite easy in the
virtual world.  If you have the hell-ban option available just use
it; perhaps there is an ignore option in your issue tracker, add a “send to
trash” rule in your email filter.  Even in person it can be quite easy to do,
just politely acknowledge their issue and move away instead of engaging them.

The solutions
-------------

I chose a solution I hate, for all intents and purposes I don’t release new Open
Source projects any longer.  I still work on a lot of projects, and the code is
normally available somewhere for strangers.  However, for the most part I’ve
made a point of not hosting or releasing it in the common places.  This works
for me, but it saddens me deeply.

I have a friend who does something interesting to combat the same problems I’ve
mentioned here.  He hooks the issue tracker to only show issues reported by
people in his second-degree FOAF_ circle or people whose user profile is an
active Open Source contributor.  It works, and it cuts out most of the problem
users, but it is nasty.  I feel it is worse than my “solution” because it still
gives the impression of support to the users you won’t support, but also gives
the impression of bad support through heaps of unanswered issues to the users
who would receive good support.

    The greatest trick the devil ever played was convincing users they had skin
    in the game.

I may be misappropriating a quote from a great film there, but it is important.
A lot of the actively poisonous people who contact you aren’t providing any real
value to you, and they’re probably never going to.  If you can remove them
somehow you’re probably not losing anything, but you’ll be gaining a whole lot
personally.

..
    There was a rant about Canonical/Ubuntu here, but I’ve decided to scrub it.
    Everyone I speak to cites the non-contributing “community member” types that
    defines the Canonical ecosystem as being a significant source of the
    poisonous user problem, but the rant is probably unnecessary outside this
    comment.

.. |API| replace:: :abbr:`API (Application Programming Interface)`
.. |GPL| replace:: :abbr:`GPL (GNU General Public License)`

.. _bikeshedding: http://en.m.wikipedia.org/wiki/bikeshedding
.. _JCB: http://www.jcb.com/
.. _Europython: https://europython.eu/
.. _FOAF: http://www.foaf-project.org/
