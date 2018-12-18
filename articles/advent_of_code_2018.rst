:date: 2018-12-15
:tags: adventofcode, coding, puzzles

Advent of Code 2018
===================

I’ve given up on |AoC| for this year, so we’ll have a ten day early
retrospective.  I’m writing this is a journal entry, more for myself than
others.  You’ve been warned!

.. note::

    As always `Advent of Code`_ is fun, even when it doesn’t always feel like
    it.  If you’re enjoying it, *or* currently screaming at it, `tip the
    creator`_ so that we can smile and shout at it next year.

Why quit?
---------

First up, I’m struggling with motivation a bit this year.  Added to that I’ve
floundered purely on the descriptions for the past couple of days, but I’m
pretty sure that it is largely my problem too.

I have 28 stars for completing both parts of every day so far this year, but
I’m haven’t been enjoying it enough to warrant continuing.

Day 1
-----

* `Chronal Calibration <https://adventofcode.com/2018/day/1>`__

As expected the first day is going to be easy.  So easy in fact you’ll regret
not getting up at 5am to race for the leaderboard.  All you have to do is sum
the numbers in your input.  The question page gives the following examples to
really hammer home the point:

    * +1, +1, +1 results in 3
    * +1, +1, -2 results in 0
    * -1, -2, -3 results in -6

If — like me — you often reach for num-utils_ at the command line then you’ll
hit an annoying failure:

.. code-block:: console

    $ numsum < inputs/day01.txt
    -142678
    $ awk '{total += $1} END {print total}' inputs/day01.txt
    474

It turns out that :command:`numsum` doesn’t like the leading ``+`` for positive
numbers, and somehow I’ve never noticed.  I’m *just about* observant enough to
notice that this was wrong though. so I didn’t submit the incorrect answer.
The question does remain though: is it better that :command:`numsum` ignores
“malformed” inputs or would a default strict mode be much nicer?

.. code-block:: console

    $ tr -d + < inputs/day01.txt | numsum
    474

Either way you probably wouldn’t really need to break out an editor to do part
one.

For part two we’re looking for the first repeat within a running sum.  I did
reach for vim_ with this, but ``awk`` at the prompt was still an option.
After completing the puzzle I dove in to tidy it a little and prepare for day
two, ending up with the following::

    from itertools import cycle

    @aoc_run({
            '+1\n-1': 0,
            '+3\n+3\n+4\n-2\n-4': 10,
            '-6\n+3\n+8\n+5\n-6': 5,
            '+7\n+7\n-2\n-7\n-4': 14,
        },
        137041
    )
    @read_data
    def shift2(inputs: Iterable[str]) -> int:
        result = 0
        seen = {0, }
        for n in cycle(map(int, inputs)):
            result += n
            if result in seen:
                return result
            else:
                seen.add(result)

.. tip::

    While it won’t make much difference in this instance we use a :class:`set`
    for our ``seen`` bucket as it provides constant-time *O(1)* lookup, whereas
    Python’s :class:`list` implementation would be linear.

So, what have we here?  Well, we’ll want some kind of test runner for the
remaining days, so I hacked up a quick decorator to run the examples.

.. image:: /.images/2018-12-15-advent_of_code.png
    :alt: |AOC| example runner output

A slightly trimmed version of it follows::

    def aoc_run(tests: Dict[str, Any], final_result: Any = None):
        err_msg = '{}({}) == {!r} != {!r}'

        def runner(fn):
            name = fn.__name__
            passed = 0
            for input_, expected in tests.items():
                result = fn(input_)
                assert result == expected, \
                    err_msg.format(name, repr(input_), result, expected)
                passed += 1

            fn_file = path.basename(fn.__wrapped__.__globals__['__file__'])
            fname = 'inputs/{}.txt'.format(path.splitext(fn_file)[0])
            with open(fname) as f:
                result = fn(f)
            if final_result:
                assert result == final_result, \
                    err_msg.format(name, 'file:' + input_, result, final_result)
                passed += 1
            else:
                print(f'{name}:', style(str(result), fg='green'))
            print(f'{name}:', style('•' * passed, fg='green'))

            return fn
        return runner

This allows us to pin a dictionary of examples to a function as a proof, and to
test our final result if we’re refactoring.  If you provide examples with no
personal solution the runner will simply display it, so that you can dump it in
to the day’s input box.

The only other interesting thing in the part two solution is that we’ve
immediately reached for :mod:`itertools`.  :func:`~itertools.cycle` allows us
to avoid implementing our own looping, and also avoid concerning ourselves with
the differences between iterators and iterables [#]_.

.. note::

    You could clearly implement the same thing with a ``while`` loop and an
    index, but this method makes the reasoning obvious(at least in my eyes).
    And that is the beauty of a lot of the helpers in :mod:`itertools`, they
    improve readability by allowing you to “code the intent”.

According to :pypi:`rdial` I could have been on the leaderboard for both parts
if I’d woken up at five to work on it :/

Day 2
-----

* `Inventory Management System <https://adventofcode.com/2018/day/2>`__

This puzzle was pretty simple too, largely just concerning a count of
characters.  Python helps here, as it provides a simple bag wrapper called
:class:`collections.Counter` that can do all the work for us.  An unedited dump
of my :pypi:`ptpython` session is below::

    def part1(inputs):
        twos = threes = 0
        for line in inputs:
            c = Counter(line)
            if 3 in c.values():
                threes += 1
            if 2 in c.values():
                twos += 1
        return twos * threes

In this instance a ``Counter`` object is simply a dictionary with characters
from the line as keys, and their frequency as values.  By simply relying on
``Counter`` and asking it whether any items are repeated two or three times
we’re barely even having to write code to solve this problem.

For part two we’re required to find matches with a substitution edit distance
of one, and return their matching characters.  :mod:`difflib` provides us with
:func:`~difflib.get_close_matches` which will the find matches for us.  For
example, we could loop over our inputs with something like the following::

    matches = get_close_matches(current, inputs, cutoff=cutoff)
    if len(matches) == 2:
        print(''.join(c1 for c1, c2 in zip(*matches) if c1 == c2))

where ``cuttoff`` is the threshold for changes, so ``(len(current) - 1)
/ len(current)`` for a single character change.

.. note::

    We’re seeing two matches here partly out of laziness, the simplifed version
    above is testing against the set of all inputs which includes the current
    word and thus always has one perfect match.

Day 3
-----

* `No Matter How You Slice It <https://adventofcode.com/2018/day/3>`__

I feel like day three is the first day this year where we’ll need to do some
actual work, but how much work we’ll need to do is dependent on our feelings on
dependencies.  A few of my co-workers *claim* it is cheating to reach for an
off the shelf solution, but as the previous sections prove I’m definitely not
in that camp.

For this puzzle we need to imagine a piece of mappable cloth, so a 2-d array is
on the cards.  If we’re using Python then we’ll need to do a lot of work to
operate on chunks of that array, but there is an easier way if we extend our
tools to include :pypi:`numpy`.

    “NumPy is a general-purpose array-processing package designed to
    efficiently manipulate large multi-dimensional arrays of arbitrary records
    without sacrificing too much speed for small multi-dimensional arrays.
    NumPy is built on the Numeric code base and adds features introduced by
    numarray as well as an extended C-API and the ability to create arrays of
    arbitrary type which also makes NumPy suitable for interfacing with
    general-purpose data-base applications.”

    -- :pypi:`numpy` project page

``numpy`` supports addressing sub-arrays with ``array[x1:x2,y1:y2]``, and
combined with its fast and efficient array creation we can solve this with low
effort.  So, we can prime an empty array and increment each element when it is
touched by elf::

    Geometry = namedtuple('Geometry', 'x, y, w h')

    data: Dict[int, Geometry] = process_input(inputs)

    grid = zeros((max_x, max_y))
    for g in data.values():
        grid[g.x:g.x + g.w, g.y:g.y + g.h] += 1
    return grid

where ``data`` is our parsed puzzle input taking advantage of
a :func:`~collections.namedtuple`.  My own solution ended up being generalised
in various ways for later use with::

    def process_input(inputs: Iterable[str]) -> Dict[int, Geometry]:
        data = {}
        for line in inputs:
            c, *geo = extract_numbers(line)
            data[c] = Geometry(*geo)
        return data

which is built upon a utility function that I wrote::

    def extract_numbers(line: str) -> Iterable[int]:
        return map(int, findall(r'[-+]?\d+', line))

There are quite a few puzzles in this and previous years where extracting all
the numbers from a string that contains other noise is useful.  In today’s
example all the lines were of the form ``#1353 @ 240,198: 29x10``, and given
that the format is stable just pulling the numbers is an entirely reasonable
way to work with it.

.. tip::

    The ``[-+]`` is there to match inputs similar to day one where positive
    numbers may be given with a leading ``+``.

Back to the problem at hand, all we need to do for part one is find the count
of array items where the value is greater than one.  Without even resorting to
more ``numpy`` goodness we can use::

    sum(1 for row in grid for col in row if col > 1)

You could perform the calculation with ``numpy`` by having it filter the
results with where_ instead of a generator.  That really doesn’t feel cleaner
in my eyes for this instance, but your taste will surely vary.

For part two we have to find a sub-array from our input that has no overlaps,
and we can simply iterate over the ``dict`` and return when we find no elements
above one::

    for id_, g in data.items():
        if grid[g.x:g.x + g.w, g.y:g.y + g.h].max() == 1:
            return id_

This time I’m showing a ``numpy`` version, but you could easily use the
built-in :func:`all` function as the worker for this depending on your taste
for ``numpy`` [#]_.

.. note::

    I’m going to recommend learning :pypi:`numpy` here irrespective of its use
    in |AOC| puzzles as it is *hugely* useful when dealing with more complex
    problems or with significantly larger inputs.  You’ll find ``numpy`` is far
    more efficient as the size of the arrays increase, and it is a nice tool to
    add to your knowledge.  In this specific instance it actually impairs the
    run-time versus cPython using a ``List[List[int]]``, but the slowdown is
    very small and the array slicing syntax more than makes up for that.

Day 4
-----

* `Repose Record <https://adventofcode.com/2018/day/4>`__

The first thing to take note of here is that while we’re given a timestamp,
we’re told we only need to care about the minutes so there is no need to
parse the whole string.  We need to keep an inventory for each guard, and
I chose to just keep two lookup tables for quicker implementation in my
:abbr:`REPL (Read–eval–print loop)`; one for the guard’s time asleep
``Dict[int, int]``, and one for minutes they sleep on ``Dict[int, List[int]]``.

Once again the standard library provides us with some functionality to make
this easier, and this time it is :mod:`collections`’s
:obj:`~collections.defaultdict`.  Instead of needing to handle adding guards
for new… er, guards we can just dynamically create dictionary items from
a default::

   guards = defaultdict(int)
   guards_minutes = defaultdict(list)

The naïve answer to processing this problem’s input is just a simple state
machine with a billion ways to implement it.  I chose this option and
produced an ugly many-armed state machine across a ``sorted(input)``, which
I’ll spare you the horror of as it contains nothing unusual or interesting.

.. note::

    While the timestamps are unused within the data the fact they’re in
    |ISO|-8601 format means we can use a default lexical sort, the problem
    would have been a little trickier had it used American mid-endian date
    formatting for example.

Once we’ve processed our input we can find the sleepiest guard::

   sleepiest = max(guards.items(), key=itemgetter(1))[0]

The ``key`` argument cause :func:`max` to sort based on the tuple’s second
element.   Using :mod:`operator`’s :func:`~operator.itemgetter` here feels
nicer than a ``lambda``, although the effect is the same.  Every time I reach
for ``itemgetter()`` or :func:`~operator.attrgetter` I yearn for quick
``lambda`` sugar, like ``C#``’s `fat arrow`_ or some such.

Then to find the minute the guard is most likely to be asleep on::

   minute = Counter(guards_minutes[sleepiest]).most_common(1)[0][0]

Once again we’re using a :class:`~collections.Counter` object, which happily
provides us with a method to find the ``n``-th most common element(one in
this case.  If the deep tuple indexing upsets you — and it does me — then you
could rewrite it in reverse order using :func:`max` or :func:`sorted`.
However, for a quick ``ptpython`` session I was happy *enough* with that.

The second part is simply just grabbing at the data with a different selector,
and contains no new functionality.

Day 5
-----

* `Alchemical Reduction <https://adventofcode.com/2018/day/5>`__

For day five we need to work our way around a string collapsing it when various
conditions match.  I chose to use a :class:`~collections.deque` for this as
a double ended queue allowed me to quickly visualise the pointer moving around,
but ``cast``\ing to a list would be a far cleaner solution.

::

    data = deque(map(ord, string), len(string))
    p = 0
    while p < (len(data) - 1):
        if data[p] ^ 0x20 == data[p + 1]:
            data.rotate(-p)
            data.popleft()
            data.popleft()
            data.rotate(p)
            p = max([0, p - 1])  # Re-align pointer
        else:
            p += 1
    return len(data)

I made the solution very dirty by working on the code points instead of the
characters as I was prematurely optimising for run-time.  The ``char ^ 0x20``
part is a bit flipping trick to invert the case of an ASCII character, and it
removes the need to test both ``Aa`` and ``aA`` for example.

.. tip::

    You could just as easily use ``str.swapcase()`` if you’re working on the
    characters directly, while also noting that doing so would handle Unicode
    and other cools things my version wouldn’t.

I’ve since benchmarked a couple of alternatives, such as iterating over
``string.ascii_lowercase`` and calling ``str.replace()`` until the
string no longer changes.  Many are simpler to reason about and perform in
roughly the same time, but for paedagogy I’ve kept the ``deque`` version here.

Anyway, it turns out I was right.  There were going to be some significant
optimisations to make this work reasonably.  However, they didn’t show up until
part two, and when they did it was easier to switch languages than acceptably
speed up the Python version.  The result using the following ``C++`` is
instantaneous on my machine, while the Python version takes about five seconds
to produce the same answer.

.. code-block:: cpp

    #include <iostream>
    #include <string>
    #include <vector>

    using namespace std;

    int react(string s) {
        vector<char> q;
        for (auto c: s) {
            if (q.empty()) {
                q.push_back(c);
            } else {
                char prev = q.back();
                if ((prev ^ 0x20) == c) {
                    q.pop_back();
                } else {
                    q.push_back(c);
                }
            }
        }
        return q.size();
    }

    int main() {
        string s;
        cin >> s;
        int ans = INT16_MAX;
        for (int i = 'a'; i <= 'z'; i++) {
            string test;
            for (char c: s) {
                if (!(c == i || (c ^ 0x20) == i)) {
                    test += c;
                }
            }
            ans = min(ans, react(test));
        }
        cout << ans << endl;
        return EXIT_SUCCESS;
    }

I’m using the same general method here; my ``deque`` in the Python version is
basically a vector anyway, and the case swapping trick is the same.

I’m showing it in full to make a point here, if you want speed in these games
use a language with loads of helpers built in and low verbosity.  Even things
like ``string.ascii_lowercase`` saves valuable seconds over making your own
iterator.

.. tip::

    A co-worker used ``qwertyuiopasdfghjklzxcvbnm`` in their solution, as it is
    faster to mash the keyboard in order than type out the alphabet.  I have to
    admit I *really* loved seeing that, and it wouldn’t have occurred to me.

Day 6
-----

* `Chronal Coordinates <https://adventofcode.com/2018/day/6>`__

Day 6 was a chore.  Sitting on the train I read a few mails from co-workers who
had landed on a bug in the puzzle that meant their correct answers wouldn’t be
accepted, and that was later clarified in a note on the leaderboard_.

With this in mind I totally ignored the puzzle until after work, at which point
I just mashed together the easiest solution I could as I didn’t want to waste
time on it.  Given it is just `Manhattan distance`_ on an map there wasn’t
anything new to see anyhow; I will note that :pypi:`scipy` contains
``scipy.spatial.distance`` which supports taxicab geometry with the
``cityblock`` parameter though [#]_.

Day 7
-----

* `The Sum of Its Parts <https://adventofcode.com/2018/day/7>`__

I’m not sure what to say about this puzzle.  If you spotted that
this was a topological sort with lexicographically broken tie breaks, you’d
probably already know that :pypi:`networkx` provides
``lexicographical_topological_sort()``.  I’m that person, and so I just called
the function for the answer.

I think this is where I started to lose interest.  Somehow I *won*, but
I really didn’t feel like I had.  That felt like cheating, and so did using
:pypi:`scipy` the day before.  As I said at the start, I’ve been lacking
motivation a little anyway and I’m not assigning *any* blame toward |AOC|
creators for this.

Day 8..14
---------

I’ve largely just been going through the motions for the past few days, and if
it hadn’t been for wishing to peacock some co-workers I’d probably have retired
earlier ;)

And that is the main reason I’m quitting, I don’t even like my own solutions
enough to write about them.  A combination of just doing the minimum required
to get *an* answer and not being interested enough to go back for refactoring.

Tips
----

I’m mostly repeating my tips from :doc:`last year <advent_of_code>`.

Don’t use this as an excuse to learn a new language.  The puzzles aren’t really
complicated enough to learn a new language beyond basic grammar.  You may as
well use it as an excuse to explore new features in a language you already
know, or as an excuse to explore the standard library of your chosen language
some more.

Read the problems *deeply*.  The artificial nature of the puzzles often elides
important information, or at least can often feel that way.  These *are*
puzzles so you should expect some vexation, and skimming for speed will make
this worse!

If you’re going for the leaderboard you need to be *really* fast, so: Use fast
languages, be *all over* your chosen weapon’s standard library, and use your
editor’s snippets_ well.  **Every**. **Second**. **Counts**.

And finally, keep your old solutions around either in files or in your |REPL|’s
history as you’ll probably end up revisiting them.

Hopes for 2019?
---------------

Moving up a place from number two last year: That the options to pay for it are
better next year.  Each year I have to find a friend to make a donation in my
place as the payment options are weak.  It would be nice to not have to do so,
and limiting payments to PayPal and Coinbase *must* be putting others off
a donation entirely.

Number two?  That it returns.  When it is fun it is *really* fun, and I just
hope I’m in a better place personally next time.

What’s next?
------------

Let us be honest here.  Winteral is almost upon us and I’ll probably end up
diving back in to complete the remaining days ;)

.. rubric:: Footnotes

.. [#] For those not too familiar with Python_ — and forgetful people like me
       — it can be easy to trip oneself up on iterators over a list repeatably,
       and then exhausting an iterable because you’re treating it as a list.
       :func:`~itertools.cycle` does the right thing either way.
.. [#] Or for that matter ``numpy``’s own ``all()`` function which becomes
       useful when using ``numpy`` for more complicated tasks.
.. [#] Yep, I’ve used three names for the same concept here to make a point
       about how annoying it can be to discuss these things when even simple
       concepts are often known by various common names.

.. |AoC| replace:: :abbr:`AoC (Advent of Code)`
.. |REPL| replace:: :abbr:`REPL (Read–eval–print loop)`

.. _Advent of Code: http://adventofcode.com/2018
.. _tip the creator: https://adventofcode.com/2018/support
.. _num-utils: http://suso.suso.org/programs/num-utils/
.. _vim: https://github.com/vim/vim/
.. _Python: https://www.python.org/
.. _where: https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.where.html
.. _fat arrow: https://en.m.wikipedia.org/wiki/Fat_comma
.. _leaderboard: https://adventofcode.com/2018/leaderboard
.. _Manhattan distance: https://en.wikipedia.org/wiki/Taxicab_geometry
.. _snippets: https://github.com/SirVer/ultisnips/
