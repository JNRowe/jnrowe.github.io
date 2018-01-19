Uber pink prompts
=================

:date: 2009-09-25
:tags: bash, styling

cookiemon5ter asks in ``#gentoo`` on Freenode:

    anyone know where to get a list of color codes for ``bash`` or know the code
    for pink :p

My first suggestion was to look at `console_codes(4)`_ for the escapes, and note
that pink isn’t defined.  As a workaround I suggested changing the console
palette using ``echo "\e]PDff1493"`` which will make the normal magenta escape
in to a much deeper pink.  The syntax to change the console colour palette is
``\eP[{colour_number}][{red}][{green}][{blue}]``, so deconstructing the above
example we are setting colour code ``D`` (or 13) to ``#ff1493``.

However, the idea cookiemon5ter had wasn’t to change the palette but just to use
a nice pink in the bash_ prompt under mrxvt_.

    i was just talking [about] editing the line in bashrc

Using ``mrxvt``, or any other terminal that supports the xterm_’s 256 colour
mode, we can actually pick a variety of pinks to use directly without having to
redefine the palette.  The prompt with a more gaudy pink can be achieved with
the following::

    export PS1='\[\e[01;33m\]\u@\h\[\e[38;5;199m\] \w\$\[\e[00m\] '

The important change here is the use of ``\e[38;5;199m``, which tells mrxvt to
select colour 199 from its extended 256 colour range.  Colours 196 through 201
are varying levels of pink.  To see a quick table of the full colour range you
can use the following little loop::

    for i in {0..15}
    do
        for j in {0..15}
        do
            col=$((i*16+j))
            printf "\e[38;5;%im %03i" $col $col
        done
        printf "\n"
    done

.. image:: /images/2009-09-25-256_colours.png
   :alt: xterm's 256 colour palette

There is one other important point to make here, you must set the prompt based
on terminal type now as some terminals and the console won’t recognise the
sequences correctly.  Test the terminal type by checking ``$TERM`` in your
startup scripts, or if you’re convinced all your terminals are 256 colour
capable you can simply check for ``$DISPLAY`` instead.

Changing the console palette and using 256 colour mode makes for two tips
today!!

.. _console_codes(4): http://kerneltrap.org/man/linux/man4/console_codes.4
.. _bash: http://cnswww.cns.cwru.edu/~chet/bash/bashtop.html
.. _mrxvt: http://materm.sourceforge.net/
.. _xterm: https://invisible-island.net/xterm/
