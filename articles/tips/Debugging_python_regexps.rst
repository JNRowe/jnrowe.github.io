Debugging Python regular expressions
====================================

:date: 2009-10-29

Rob Sampson is learning Python_ and struggling to get to grips with its
|RegEx| handling.  He asks on one of our internal lists at the office:

    I've written what I believe to be a valid |RegEx| to perform matches on
    some data, and I can't figure out why it isn't matching on my input.
    Any clues about where to look?

The answer to these types of questions is more often than not one of two things:

1. Failure to use `raw strings`_ when including backslashes in the |RegEx|

2. Choosing to use a |RegEx| when a better tool for the job exists

Raw strings
-----------

In Rob's code he had failed to take in to account the backslash escaping
problem.  A simplified example of what he was trying to do would be:

.. code-block:: pycon

    >>> import re
    >>> re.findall(' ([0-9]+\\[a-z]+) ', 'make 123\match ')
    []
    >>> # Whereas with raw strings this match will work
    >>> re.findall(r' ([0-9]+\\[a-z]+) ', 'make 123\match ')
    ['123\\match']

`Fork this code <http://gist.github.com/198015>`__

Without the raw string, specified by the preceding ``r`` in our pattern, the
|RegEx| parser is actually looking for a literal ``[`` where we've intended
to use the ``[`` as the start of a character set.

.. note::
   There is another important point here too as the example above uses
   character ranges, just as Rob's original did.  As in most |RegEx| engines
   Python has inbuilt support for certain character classes, and they are
   often more functional than the simple character ranges.  The big win with
   Python's character classes is that they can be locale and/or Unicode
   aware by specifying the LOCALE_ or UNICODE_ flags.

These types of string escaping problems are common, and as your |RegEx|
becomes more complex their likelihood increases greatly.  Python, as is often
the case, has the answer and it comes in the shape of the ``re.DEBUG`` flag
which unfortunately appears to not be documented.  The ``re.DEBUG`` flag
displays a parse tree allowing you to easily inspect the |RegEx| you have
constructed:

.. code-block:: pycon

    >>> re.findall(' ([0-9]+\\[a-z]+) ', 'make 123\match ', re.DEBUG)
    literal 32
    subpattern 1
    max_repeat 1 65535
        in
        range (48, 57)
    literal 91
    literal 97
    literal 45
    literal 122
    max_repeat 1 65535
        literal 93
    literal 32
    []

`Fork this code <http://gist.github.com/223892>`__

Here we can see that our expression matches ``range (48, 57)``, 48 and 57 being
the ordinal_ for ``0`` and ``9`` respectively.  Following that we see a match
for ``literal 91``, ``chr(91)`` shows us that the character we are matching is
a ``[``.  With this information it is easy to see where the problem is.

If you need to use more than one flag, such as often useful VERBOSE_ flag, you
can combine them with ``|`` (bitwise OR) as the flags are just named
constants(``DEBUG`` is 128 for example).

.. code-block:: pycon

    >>> re.findall(r' (\d+\\\w+) ', 'make 123\match ', re.DEBUG|re.LOCALE)
    literal 32
    subpattern 1
    max_repeat 1 65535
        in
        category category_digit
    literal 92
    max_repeat 1 65535
        in
        category category_word
    literal 32
    ['123\\match']

`Fork this code <http://gist.github.com/223893>`__

Better tools
------------

Often, a |RegEx| is the hammer of choice for far too many tasks for far too
many people(myself included).  There are often much better choices, some of
which are very domain specific and some quite general.

For any moderately complex parsing job pyparsing_ is a great choice.  The
syntax is quite readable and the parser is very fast.  Just make sure you
ignore any examples telling you to use ``from pyparsing import *`` as you'll
evoke great rage in every person who reads your code.

While ``pyparsing`` is a good general parsing tool it would be overkill for
the task at hand, but it doesn't hurt to show a simple example of
constructing a parser:

.. code-block:: pycon

    >>> from pyparsing import (Literal, White, Word, alphas, nums)
    >>> matcher = Word(alphas) + Word(nums) + Literal('\\') + Word(alphas) + White()
    >>> matcher.parseString('make 123\\match ')
    (['make', '123', '\\', 'match', ' '], {})

`Fork this code <http://gist.github.com/223894>`__

Another exceptional tool for tasks that people often abuse |RegEx| for is
python-dateutil_.  One of the reasons I occasionally turn to this module is
that Python's time.strptime_ isn't even capable of parsing timestamps created
by time.strftime_, for example if you use ``%z`` in the ``strftime`` call.

All too often you see people trying to solve date parsing problems with
|RegEx| and heaps of int_ calls to mangle the matches.  Not only is this
a very brittle approach, but the labix_ guys have solved this problem for you
already:

.. code-block:: pycon

    >>> from dateutil import parser
    >>> s = '2009 10 30 23:35:16+0400'
    >>> parser.parse(s)
    datetime.datetime(2009, 10, 30, 23, 35, 16, tzinfo=tzoffset(None, 14400))

`Fork this code <http://gist.github.com/223895>`__

.. note::
   If you use `python-dateutil`_ do be aware that by default it will prefer US
   mid-endian date formats when guessing for some patterns.  Either create your
   own ``parserinfo`` object and set ``dayfirst`` to ``True``, or use something
   stricter.

In closing before you start parsing any text -- regardless of how simple it
is -- you should thumb through the `standard library`_ and perform a search
on pypi_.  Often, the work has already been done for you and may well be much
better than the hurried version you were about to cobble together with
a |RegEx|.

.. _Python: http://www.python.org/
.. _raw strings: http://docs.python.org/tutorial/introduction.html#strings
.. _LOCALE: http://docs.python.org/library/re.html#re.LOCALE
.. _UNICODE: http://docs.python.org/library/re.html#re.LOCALE
.. _ordinal: http://docs.python.org/library/functions.html
.. _VERBOSE: http://docs.python.org/library/re.html#re.X
.. _pyparsing: http://pyparsing.wikispaces.com/
.. _python-dateutil: http://labix.org/python-dateutil
.. _time.strptime: http://docs.python.org/library/time.html#time.strptime
.. _time.strftime: http://docs.python.org/library/time.html#time.strftime
.. _int: http://docs.python.org/library/functions.html#int
.. _labix: http://labix.org/
.. _standard library: http://docs.python.org/library/
.. _pypi: http://pypi.python.org/pypi
