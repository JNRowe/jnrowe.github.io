.. post:: 2018-10-19
   :tags: adventofcode, coding, puzzles
   :image: 1

Advent of Code 2017
===================

A very evil friend pointed me to `Advent of Code`_ last December, and I burnt
a fair chunk of time on it.  I mean… yeah, it *was* hugely fun but be warned it
is enormously addictive [#]_.

.. important::

    I must say that I meant to write this last December, but things got in the
    way and writing doesn’t earn me enough valuable Internet points.  Don’t
    take this being 10 months late as a knock against |AOC|, but more as me
    thinking we’re on the cusp of a one month countdown to it beginning
    again(hopefully).

Why?
----

This answer should be obvious; puzzles are fun, competitive ones where you
prove yourself against co-workers and *total* strangers even more so.  If that
isn’t enough reason to have a go, then I simply don’t want to know you.

Lessons
-------

It is huge fun, but if you want to get on the leaderboards you *must* be up
when the puzzle is released.  Sadly, in the UK that means waking up for
a **five in the morning** start.

If you look at my completion screenshot, you’ll also see I have the
:mod:`itertools` documentation open.  If you’re going to use Python for |AOC|
study up on :mod:`itertools`, it will help no end [#]_.

.. image:: /.images/2017-12-29-advent_of_code.png
    :alt: Ta-da! Calendar complete
    :scale: 50%

The other thing you can see in my screenshot is that I didn’t complete the
event on Christmas Day, in fact I took a break and finally mashed through the
final week on the evening of the 28th.  Infinite time, unemployment or being
smarter would be a great help here.

Approach
--------

With the exception of one day — where the answer just jumped out at me — I used
exactly the same approach.  Whack out *a* solution for the given samples that
tested green, then chuck in my magic string to get a hopefully correct answer
to submit.  Once successful I’d return to the code to clean it up, and also to
think through the problems a bit more.  As with many things in life, there can
be a lot to learn through posthockery.

If we look at the description for `day 1`_:

   The captcha requires you to review a sequence of digits (your puzzle input)
   and find the sum of all digits that match the next digit in the list. The
   list is circular, so the digit after the last digit is the first digit in
   the list.

   For example:

   - 1122 produces a sum of 3 ( 1 + 2) because the first digit ( 1) matches the
     second digit and the third digit (2) matches the fourth digit.
   - 1111 produces 4 because each digit (all 1) matches the next.
   - 1234 produces 0 because no digit matches the next.
   - 91212129 produces 9 because the only digit that matches the next one is
     the last digit, 9.

I immediately dumped the samples in to a Python :mod:`doctest` file as::

    """
    >>> captcha('1122')
    3
    >>> captcha('1111')
    4
    >>> captcha('1234')
    0
    >>> captcha('91212129')
    9
    """

Now we’ll know we’re on the right track when ``python3 -m doctest day01.py``
stops spitting out errors.  Looking at my git repository it looks like my first
dirty solution was::

   @str_to_ints
   def captcha(ints):
      total = 0
      for n, last in zip(ints, [ints[-1], ] + ints[:-1]):
         if n == last:
               total += n

      return total

You’ll notice I’ve slapped a decorator on the function, with the assumption
that I’ll want to convert an iterable to integers again before the month is
out(I was right).  Its implementation was a rather basic::

   def str_to_ints(fn):
      def wrapper(s):
         ints = [int(c) for c in s]
         return fn(ints)
      return wrapper

Eagle-eyed Pythonistas will spot the horrific error here, I forgot that
decorators will wipe out my docstring and the :mod:`doctest` runner won’t pick
up my ``captcha`` tests at all.  The solution is to reach for
:func:`functools.wraps` and a tiny edit:

.. code-block:: diff

    --- a
    +++ b
    @@ -1,2 +1,3 @@
     def str_to_ints(fn):
    +    @wraps(fn)
         def wrapper(s):

I know full well that this is a better solution than diving in to the |REPL|
for me.  I tend toward `code golfing`_ myself in a |REPL|, so I’d end up with
something more like this:

.. code-block:: pycon

    >>> i1, i2 = tee(map(int, '91212129'), 2)
    >>> sum(x for x, y in zip(i1, islice(cycle(i2), 1, None)) if x == y)

I wish I could say this was made up to prove a point, but that is a chunk from
my ptpython_ history when I was playing around trying to think of a “cleaner”
solution after getting the correct answer [#]_.

I followed the same basic pattern for each puzzle, always using the same file
for part one and part two of the puzzles.  Occasionally needing to refine my
part one solution for an edge case that part two exposed.  I’ll spare you the
blow-by-blow of the other 24 days, as frankly the code is the least interesting
part of the puzzles in my opinion.

Implementation
--------------

.. figure:: /.images/2018-10-19-aoc_calendar.png
    :alt: Languages used for tasks
    :scale: 50%

    Language frequency for |AOC| puzzles

    ======  ========  =========
    Colour  Language  Frequency
    ======  ========  =========
    red     Python_   11
    blue    PyPY_     4
    green   nim_      5
    yellow  lua_      4
    ======  ========  =========

I used Python_ for over half the days, PyPY_ for a few where my immediate
thought was to reach for brute forcing a solution with a naïve algorithm, lua_
via luaprompt_ on one day where it was clear all I really needed was
a calculator, and nim_ on five days where I was using my Winterval break to
learn nim_.

Results
-------

I only made it on to the leaderboard once, and I was excited.

    Got myself on the #aoc leaderboard this morning(#91)… now back to sleep
    as its 5am 😴 http://adventofcode.com/2017/leaderboard/day/9

    -- :µnote:`2017-12-09T05:22:29+00:00`

I like to think I could have done better if it didn’t require getting up at
five in the morning to compete, but that is the just the lie I’m telling myself
to feel better.

All told, I spent nine hours on |AOC| and those hours were spread pretty evenly
between the “live” 2017 puzzles and the previous years.  I’m up for calling it
personal development, and I’m hoping it returns this year!

Tips
----

Honestly, I’m going to push against the grain on this.  All my co-workers who
have commented on this have said |AOC| is a great way to learn a new language,
but I massively disagree.  Even if you ignore the leaderboard, you’re only
making tiny little one-off programs without the need for any real design.
Granted you can learn some of the basics quite well, but it feels closer to
doing a few `“hello world”`_ implementations.  The puzzles themselves are more
in depth than “Hello world” for sure, but the implementations aren’t likely to
be very interesting or didactically useful.

*Read* the problems and *think* first, obvious I know… but when the stopwatch
is running it is easy to jump to the editor.  For example, `day 12`_ is clearly
pretty easy to solve by reaching for new code, but even easier to solve with
graphviz_.  In this specific instance you can use sed_ to fiddle the input,
``ccomps`` to filter the input for the ``0`` node, and finally use ``gc`` to
count the nodes [#]_.  I’ll admit here the code I used to submit my answer was
all new, and I didn’t use graphviz_ until I thought about how to refactor my
20 lines of Python.  I did use graphviz_ to solve `day 24`_’s puzzle, so
even I *can* learn from my own advice on occasion.

I used moonscript_ for `day 21`_, which was a mistake because the syntax wasn’t
a good fit.  It would have been faster, shorter and cleaner to use Haskell, as
I did when I reworked it after submitting.  Really, this is the same point as
the last but should be repeated: *think* first, *appropriate* tools matter.

If you’re going for the leaderboard you need to be *really* fast, so: Use fast
languages, be *all over* your chosen weapon’s standard library, and use your
editor’s snippets_ well.  **Every**. **Second**. **Counts**.

And finally, keep your old solutions around either in files or in your |REPL|’s
history as you might end up revisiting them, as was the case with `day 14`_ for
example.

Hopes for 2018?
---------------

Number one?  That it returns.  It was a great deal of fun.  It spawned a fair
amount of interesting water cooler chat too.

Number two?  That the options to pay for it are better this year.  Last year
I had a friend tip some money towards the AOC++ scheme in my place, as the
available options wouldn’t work for me at all.

If I had a number three it would be to figure out a way to make it work without
having to get up at five, I just can’t even imagine what that could be.

.. rubric:: Footnotes

.. [#] More so as the puzzles from previous years are still online, so you can
       end up sucked in to old puzzles very easily.
.. [#] Frankly, I’m of the strong opinion that you should be studying up on
       ``itertools`` *all* the time anyway.  It just that other Python
       developers aren’t always familiar enough with the module for use in
       large shared code bases, so help to make this a reality!
.. [#] For some value of “cleaner” which is both unique to me and a totally
       untrue.
.. [#] In fact, this tip isn’t specific to |AOC| at all.  Just stop reading
       now and learn to use graphviz_, it can be used to solve so *many*
       engineering problems.

.. |AoC| replace:: :abbr:`AoC (Advent of Code)`

.. _Advent of Code: http://adventofcode.com/
.. _day 1: https://adventofcode.com/2017/day/1
.. _code golfing: https://en.m.wikipedia.org/wiki/Code_golf
.. _ptpython: https://pypi.org/project/ptpython/
.. _Python: https://www.python.org/
.. _PyPY: http://pypy.org/
.. _lua: http://www.lua.org/
.. _luaprompt: https://github.com/dpapavas/luaprompt
.. _nim: https://nim-lang.org/
.. _“hello world”: https://en.m.wikipedia.org/wiki/%22Hello,_World!%22_program
.. _day 12: https://adventofcode.com/2017/day/12
.. _graphviz: https://www.graphviz.org/
.. _sed: http://sed.sourceforge.net/
.. _day 24: https://adventofcode.com/2017/day/24
.. _moonscript: https://github.com/leafo/moonscript/
.. _day 21: https://adventofcode.com/2017/day/21
.. _snippets: https://github.com/SirVer/ultisnips
.. _day 14: https://adventofcode.com/2017/day/14

.. spelling::

    AOC
    Pythonistas
    aoc
    docstring
    iterable
    leaderboard
    leaderboards
    posthockery
    th
