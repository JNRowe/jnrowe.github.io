.. post:: 2018-12-04
   :tags: tools, projects, languages
   :image: 1

Giddy new project love
======================

I’ve recently inherited a new tier-one project, which is great news!  Sadly, it
is in real need of some Tender Loving Care™.  Was there ever an inherited
project that wasn’t?

The project is our semi-custom transpiler for Ada_ affectionately called
``sandfly``.  I say semi-custom as it was spun out from a consortium effort to
“facilitate reliability and improve portability” of ``Ada`` projects, which is
a far loftier sounding goal than it need be.  In essence, it is the
codification of rules and guidelines we’ve adhered to since a partner meeting
in *1996*, and that we find ourselves still following today [#]_.

I wasn’t around back when the original group was formed, and it was disbanded
before I’d even heard of ``Ada``.  This project is genuinely
multi-generational, which *feels* nice.  All too often our work in software can
feel ephemeral; squeaked on a whiteboard in the morning, tapped in to
a computer in the afternoon and swept away by the janitors as night falls.

Hopes and dreams
----------------

As the project *should* have significant longevity I find myself pondering the
future.  *If* I could change things for the next 20 years, what should I do to
make that experience better?  Should I do *nothing at all* and just chug along
reducing the anxiety that even small changes will evoke?

I also find myself pondering the present.  Could a truly radical change *today*
obviate the need for this project entirely before the next maintainer grabs the
reins for their reign of anxiety?  Would that necessarily be a good thing?

.. sidebar:: Common errors

    I’ve always considered it odd that we can choose to attach a listing of
    common errors to a product and expect people to use it.  If we know it is
    common for users to make critical errors because of a design decision we
    need to make a new design, not a new bullet point on the list.

    Even simple things like watching an ``Ada`` beginner make the classic
    “atomic means atomic” mistake should be designed out, and not *solved* with
    an addendum of “protected objects mean atomic” chicanery.

Many of the advantages that we associate with ``Ada`` — such as its mighty type
safety — no longer feel that advanced or remotely unique.  Even “hobby”
languages such as nim_ implement many of the safety features we expect from
``Ada`` implementations [#]_; subrange types being a fine example where the
``nim`` designers have absorbed an ``Ada`` feature.  And standard everyday
languages now often have tooling that is capable of providing *many* of the
benefits of ``Ada``, and one should really only expect this to increase.

What really hammers home the point here is that a good number of the features
one thinks about weren’t even available in ``Ada`` when ``sandfly`` began; fex
contracts are from `Ada 2012`_.  Will languages leapfrog ``Ada`` in its niche
by borrowing and then sprint away by innovating as their uptake increases?

Benefits of transpilation
-------------------------

The original ``sandfly`` authors implemented a transpiler because it made
various checks simpler to carry out.  According to the documentation, it was
never intended to become a full blown language in its own right… which of
course it has.

Maybe we should take the opportunity to stay on top of the changing language
landscape thanks to the side effect of ``sandfly``’s implementation details.
Given that we’re already transpiling should we consider alternative targets?
ocaml_ is the language that immediately jumps to mind, as it is syntactically
close to ``sandfly`` and it has an excellent type system.  And once you have
``ocaml`` it is a smaller step to `F#`_ thanks to its legacy ``ocaml`` mode.

The code base is amenable to multiple targets already.  A couple of years ago
I implemented support for testing without relying on the support kernel
supplied by our compiler vendor [#]_.  At its base ``sandfly`` will optionally
generate lua_ bytecode that is loaded in to a tiny emulator which can be driven
by other ``lua`` scripts to test an implementation.  Its main purpose was to
allow early experimentation without the expense and time of waiting for
hardware re-fabrication.

.. figure:: /.images/sandfly_use.png
   :scale: 50%
   :alt: sandfly debug architecture

   As you can see from example usage, it’s source-to-source all the way down.
   If I’m writing ``lua`` I’m using moonscript_, and so should you!

I’m not sure it would even be a great stretch to change the main target, there
would likely be significant support for it in fact.  It has already been
suggested that we should exclusively switch to spark_ on a number of occasions,
especially since the reformation in Spark 2014.  If we could figure out the
safety certification story I’m sure there would be a lot of traction for ``F#``
as default.

Final thoughts
--------------

.. sidebar:: Open Sourcing ``sandfly``

    There have been a few enquiries as to whether this work is Open Source, and
    sadly it isn’t.  However, if you work for one of the Atlas Consortium
    companies(or a significant partner of one) it is easy to arrange “source
    available” access.  I *know* this isn’t the same thing, but it is the
    current situation.

    The good news is that I’ve added an item to the issue tracker that includes
    making it Open Source, the bad news is that there is a lot of work needed
    — both by me and *many* others — to make that happen.  I’ve kicked the
    initial process off by contacting legal for guidance, we’ll see what
    happens.

I’ve always really appreciated vala_\’s alternative syntax support; `C#`_ by
default, but with first class support for genie_\’s boo_-inspired syntax.
I find myself thinking how nice it would be to emulate that and have multiple
frontends, *and* the previously described backends.

In fact I find myself thinking about ``vala`` a lot as I write this.  It never
had the uptake I would have hoped for when I first read about it.  It has
however had a *huge* impact in the places where it has been used.  That surely
makes it a great role model for ``sandfly`` going forward.  It is better to be
an elusive Aston Martin DB-5_ than a common as muck `Ford Focus`_.

So, I’m deep in a pre-reality dream state where I want to add heaps of amazing
new features and functionality, coupled with a cold light of day feeling that
it could be nice to kill the project by transforming it in to a gateway out of
``Ada``.  It could be the best *or* worst project in the history of the world!
I’m genuinely excited.

.. rubric:: Footnotes

.. [#] It should be easy to guess why this project is being handed on, given
       that we’re talking about a twenty-one year old endeavour.

.. [#] This isn’t meant to disparage nim_, as it is really quite interesting.
       I mean it purely in the sense that we haven’t *yet* seen large industry
       adoption.

.. [#] I’m of the *strong* opinion that vendors who forbid you from naming,
       shaming and even benchmarking them should be avoided at *all costs*.
       However, I’m not on the procurement board and didn’t get to make that
       decision.

.. _Ada: https://en.m.wikipedia.org/wiki/Ada_(programming_language)
.. _nim: https://nim-lang.org/
.. _Ada 2012: http://www.ada2012.org/
.. _ocaml: http://www.ocaml.org/
.. _F#: http://fsharp.org/
.. _lua: http://www.lua.org/
.. _moonscript: https://github.com/leafo/moonscript/
.. _spark: https://en.m.wikipedia.org/wiki/SPARK_(programming_language)
.. _vala: https://en.m.wikipedia.org/wiki/Vala_(programming_language)
.. _C#: https://en.m.wikipedia.org/wiki/C_Sharp_(programming_language)
.. _genie: https://en.m.wikipedia.org/wiki/Genie_(programming_language)
.. _boo: http://boo-lang.org/
.. _DB-5: https://en.m.wikipedia.org/wiki/Aston_Martin_DB5
.. _Ford Focus: https://en.m.wikipedia.org/wiki/Ford_Focus

.. spelling::

    backends
    fex
    transpilation
