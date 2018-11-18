.. post:: 2018-11-13
   :tags: linux, dzen
   :image: 4

Visualising the progress of time
================================

.. image:: /.images/time_progress.jpg
   :alt: Screenshot of Progress Bar OSX in action
   :target: https://www.progressbarosx.com/

A co-worker was demoing a user session today, and pointed out a neat tool for
MacOS that displays the “continual march toward death”.  That tool was
`Progress Bar OSX`_, and it is pretty cool.  Sadly it is only available for
MacOS, so we’ll need to make something similar.

.. raw:: html

    <div class="h-review">
        <p>
            <span class="p-name">
                <em>All</em> popup problems on
                <span class="p-category">Linux</span>
                should be solved with
                <a href="https://github.com/robm/dzen" class"p-item h-item">
                    dzen
                </a>
            </span>, it is
            <data class="p-rating" value="5">awesome</data>.
            <span class="e-content">
                You know this because it comes equipped with the option to
                produce
                <abbr title="Knight Industries Two Thousand">KITT</abbr>
                <a href="https://en.m.wikipedia.org/wiki/KITT">
                    Anamorphic Equalizer</a>
                emulation.
            </span>
        </p>
    </div>

.. figure:: /.images/kitt06.png
   :alt: Multi-band scanner in action
   :target: ../_static/kitt.gif

   Click the image for an animated GIF, I’ll spare you the flashing lights in
   case you wish to read on.

Step one
--------

First we’ll want to display the year:

.. code-block:: sh

   gdbar -w 1500 -h 20 \
      <<< $(($(date +%j) / $(date -d'Dec 31' +%j).0 * 100)) \
      | dzen2 -p 5

which results in:

.. image:: /.images/day_bar.png
   :alt: Screenshot of simple day of year bar on 2018-11-13

The logic should be simple enough to follow:

* ``current day in year`` [#]_ / ``number of days in year`` [#]_ * ``100`` for
  position in year as percentage
* Generate the :command:`dzen2` markup for a bar of ``1500`` pixels wide and
  ``20`` pixels high
* Display it for for ``5`` seconds

.. warning::

   Be sure to notice that we force ``number of days in year`` to be a float
   with the addition of ``.0``.  Without it the result would be rounded toward
   zero, ie zero on every day but December 31ˢᵗ.

We can repeat the same process for day ratio; using ``date -d "00:00" +%s`` to
calculate number of seconds passed from the 86400 we’ll see today.  And then
simply using ``date +%m`` to get today’s month as a number.

Step two
--------

We can definitely up our game here.  Why not use colours?  We’ll switch to
Python_ now, as the gigantic standard library allows us to be lazy.

::

    def pcnt_colour(percent):
        h = 1/3 - (1/3 * percent/100)
        return '#' + ''.join(f'{min(int(n*256), 255):02x}'
                             for n in colorsys.hls_to_rgb(h, .5, 1))

The function above converts a percentage value in to a hex triplet across
a green to red gradient, we use :func:`~colorsys.hls_to_rgb` here as the `HLS
colour space`_ is more amenable to generating smooth gradients.

Now that we’re using Python_ we may as well take advantage of its
:mod:`calendar` module::

    def month_days(date):
        return calendar.monthrange(date.year, date.month)[1]

The :func:`~calendar.monthrange` function returns a tuple where the second item
is the number of days in the current month.

::

    def days_in_year(date):
        if calendar.isleap(date.year):
            days = 366
        else:
            days = 365
        return days

:func:`~calendar.isleap` allows us to offload figuring out whether 2700 is
a leap year once senility begins to set in.

::

    def show_progress(title, percent, width):
        subprocess.run(['gdbar', '-l', title, '-w', str(width), '-fg',
                        pcnt_colour(percent)],
                       input=str(percent).encode())

We’ll also create a utility function to generate the :command:`dzen2` markup
required to output our little blocks of data.

Putting it altogether we can display our pretty little blocks with something
like the following:

.. code-block:: shell

    ./time_progress.py -w 1500 \
        | dzen2 -l 3 -p 3 -fn monospace-15 -e 'onstart=uncollapse'

This creates the markup and makes :command:`dzen2` display the output for
3 seconds.

.. image:: /.images/progress_bar.png
   :alt: Screenshot of colourful progress in time

The ``onstart=uncollapse`` attribute tell :command:`dzen2` that we want to see
the full output on startup, without it we’d see just the title bar until we
moved our pointer over the header.

Step four
---------

You can find the script I used :download:`here <time_progress.py>`.  It isn’t
pretty, but it will do.  If I come to depend on it I’m sure that I’ll make
something better.

I think it is important to note that if you’ve got this far and you’re thinking
about doing this yourself you should consider buying the `Progress Bar OSX`_
app.  This document wouldn’t exist without it and rewarding creators is
important, even when they ignore your chosen platform ;)

Step ∞
------

As always with any code that touches dates `“Here be dragons”`_.  For example,
I’ll leave it as an exercise for the reader how to handle calculations for days
with :abbr:`DST (Daylight Saving Time)` transitions.

.. rubric:: Footnotes

.. [#] :command:`date`’s :option:`%j` format gives us the day of year, see
       :manpage:`strftime(3)` if this is new to you.
.. [#] Calculating the day of year for December 31ˢᵗ allows to work in leap
       years.

.. _Progress Bar OSX: https://www.progressbarosx.com/
.. _Python: https://www.python.org/
.. _HLS colour space: https://en.m.wikipedia.org/wiki/HLS_color_space
.. _“Here be dragons”: https://en.m.wikipedia.org/wiki/Here_be_dragons
