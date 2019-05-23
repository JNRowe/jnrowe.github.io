.. post:: 2018-09-15
   :tags: vim
   :excerpt: 2

Vim with day/night colourschemes
================================

The fabulous Miss Biddulph asks via our EADS Linux list:

    I lurve taqua_ in vim_ during the day, but now the days are getting shorter
    it is beginning to destroy me.  Is there a way to make :command:`vim` use
    different colourschemes depending on time?

So, like most things this can either be *really* simple or horribly convoluted
depending on where you wish to draw the usability line.  Because Laura is
asking, we’ll scratch the surface of a few odd ways to do this.

The simple solution
-------------------

In many ways this is related to my awesome-timed-wallpaper_ hack, and to start
with I’m going to proceed in a similar way.

The snippet below will configure the background_ and colourscheme_ depending on
the time of day.  You can change the bounds in any way you see fit [#]_.

.. code-block:: vim

    let hour = strftime('%H')
    if hour >= 18
        set background=dark
        colorscheme jnrowe  " Best theme
    elseif hour >= 9
        set background=light
        colorscheme taqua
    else
        " Midnight to 08:59
        set background=dark
        colorscheme monokai
    endif

If you (re-)start :command:`vim` regularly this is all you’ll probably need.
If — like me — you have *very* long running :command:`vim` sessions, you’ll have
to put in some more effort to make it work:

• The easiest option would be `binding it to a key`_ and triggering it when you
  notice eye strain
• Use vim 8’s new asynchronous timer support, see ``:h timer`` [#]_
• Support pre-v8 vim by adding an autocmd_ on CursorHold_
• Script vim externally using vim’s `client server support`_
• …
• Create a systemd_ user timer that triggers at a given time ;)

The ridiculous solution
-----------------------

We’ll need to figure out the actual daylight state.  There are an enormous
number of options available.

With Python
'''''''''''

My upoints_ package can calculate sunrise and sunset:

.. code-block:: python

    >>> from upoints.point import Point
    >>> p = Point(52.2, 0.2)
    >>> p.sun_events()  # UTC results
    (datetime.time(5, 32), datetime.time(18, 15))
    >>> p.sun_events(zenith='civil')   # twilight
    (datetime.time(4, 58), datetime.time(18, 49))

With ``redshift``
'''''''''''''''''

If you already use redshift_ — and you should — getting the current state is
quite easy.  Below is example output, and a quick sed_-based method to parse the
output for script usage:

.. code-block:: sh

    $ redshift -p
    Waiting for current location to become available...
    Location: 52.2 N, 0.2 E
    Period: Night
    Colour temperature: 4500K
    Brightness: 1.00
    $ redshift -p 2>/dev/null | sed -E '/:/s,(.*): (.*),\U\1\E="\2", ; s,(\b) (\b),\1_\2,g'
    PERIOD="Night"
    COLOUR_TEMPERATURE="4500K"
    BRIGHTNESS="1.00"

Another option might be to use :command:`redshift`’s hook support, see the man
page for how to configure hooks.

.. code-block:: sh

    #!/bin/zsh

    case $1 {
    (period-changed)
        case $3 {
        (day) { notify-send "Make bright" } ;;
        (night) { notify-send "Make dark" } ;;
        }
    }

Camera input
''''''''''''

Assuming you have access to either a very good or *very* bad webcam you could
even script support that takes in to account cloud cover, or occultation caused
by buildings and trees.

For example, ImageMagick_ can be used to `extract brightness`_ from an image.

.. code-block:: shell-session

    $ curl $cam_url \
        | convert - -colorspace Gray -format "%[fx:quantumrange*image.mean]" info:
    38244.2
    $ convert pattern:GRAY0 -format "%[fx:quantumrange*image.mean]" info:
    0
    $ convert pattern:GRAY100 -format "%[fx:quantumrange*image.mean]" info:
    65535

.. note::

    As can be seen from the black(``GRAY0``) and white(``GRAY100``) examples,
    the result on *my* system is a value between 0 and 65535.  You should take
    note that ``quantumrange`` is a compile time depth setting; it can be
    queried with the ``%q`` escape, or by checking the ``Q`` value in the
    ``convert --version`` output.

The above will only really work with very poor webcams that don’t attempt to
autobalance their images, with reasonable devices it will be close to useless.

However, if you have a good quality camera image you may be able to extract the
balancing data used from the image tags, and use that to infer the light level.
exiv2_ is great option to extract that data when available, and also supports
`gobject introspection`_ making it possible to use it with lgi_ in awesomewm_
for desktop colours too!

Thoughts
--------

That is definitely enough of that rabbit hole for me right now… I’m really
looking forward to seeing people code golf some other solutions, be they useful
or [hopefully] intriguing variations.

.. rubric:: Footnotes

.. [#] If you need more branches you can also wonder why ``vimscript`` doesn’t
       have a switch statement.
.. [#] No |HTML| link, as vimdoc is still on vim 7.3

.. _taqua: https://www.vim.org/scripts/script.php?script_id=594
.. _vim: http://www.vim.org
.. _awesome-timed-wallpaper: https://github.com/JNRowe/awesome-timed-wallpaper/
.. _background: http://vimdoc.sourceforge.net/htmldoc/options.html#'background'
.. _colourscheme: http://vimdoc.sourceforge.net/htmldoc/syntax.html#:colorscheme
.. _binding it to a key: http://vimdoc.sourceforge.net/htmldoc/map.html#:nmap
.. _autocmd: http://vimdoc.sourceforge.net/htmldoc/autocmd.html#:autocmd
.. _CursorHold: http://vimdoc.sourceforge.net/htmldoc/autocmd.html#CursorHold
.. _client server support: http://vimdoc.sourceforge.net/htmldoc/remote.html#--remote-send
.. _systemd: https://www.freedesktop.org/wiki/Software/systemd
.. _upoints: https://pypi.org/project/upoints/
.. _redshift: http://jonls.dk/redshift/
.. _sed: http://sed.sourceforge.net/
.. _ImageMagick: https://www.imagemagick.org/
.. _extract brightness: https://www.imagemagick.org/script/escape.php
.. _exiv2: http://www.exiv2.org/
.. _gobject introspection: https://wiki.gnome.org/Projects/GObjectIntrospection
.. _lgi: https://github.com/pavouk/lgi
.. _awesomewm: https://awesomewm.org/

