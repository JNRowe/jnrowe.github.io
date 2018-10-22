.. post:: 2018-10-08
   :tags: desktop, tiling, tabbed

Tiling vs tabbing
=================

A fairly large chunk of my developer friends fawn over tmux_ and tabbed_.
These tools can give *the effect* of a multiple window interface to your
terminal sessions, or apply a tabbed interface to any xembed_ supporting
application respectively.  I’ll freely admit they’re pretty awesome at what
they do [#]_.

That said, I’ve never been a fan of them or the plethora of tools like them.
They feel, to me, like they’re attacking the problem from entirely the wrong
side.  Instead of configuring individual applications to behave in a tabbed and
custom way, why not just rely on that behaviour globally?  Allow me to
illustrate with the following examples.

.. image:: /.images/2018-10-08-tiling.jpg
    :alt: Example of awesomewm’s tile.right layout

If I want two terminals next to each other I’ll just switch to a layout that
supports that(in awesomewm_ I’d probably choose ``tile.right``) .  If I want
various image viewer windows open and a nice tabbed interface to access them,
I’ll just tag them all and enable a layout that supports that(such as dwm_’s
monocle [#]_).  If I want to vertically split a terminal window and then
horizontally split that to include a ``vim`` instance, I can just tag those
three windows and enable a layout that supports it [#]_.  I think the basic
message should be clear by now.

.. sidebar:: Window manager choice

    I’ve used both awesomewm_ and dwm_ as examples here because I use both
    depending on what machine I’m in front of.

    However, you can achieve the same effect with any number of tiling window
    managers, or with tools like winwrangler_ [#]_ if your favourite window
    manager has weaker layout management.

You can go further too.  Say you want ``vim`` and a browser window side by side
while reading documentation but need that ``vim`` instance next to a terminal
for running tests, then you can simply apply two tags to the ``vim`` instance
and switch between both layouts with a rattle of the keyboard.  The exact same
interface you’d use for any other layout change too, not one that is specific
to ``tmux`` or ``tabbed``.

It seems strange to me that given the option to performs tasks like this at the
window manager level people would *choose* to insert an extra layer in the
middle that does less.  By using actual windows you sidestep the problems with
mouse selection in pseudo-windows in ``tmux``, and you can change your mind
about your preference for tabs or tiling mid-session unlike with ``tabbed``.

You can also abuse other excellent things like xdotool_ to fiddle with your
layout or interact with specific clients instead of needing to do application
specific things depending on whether you’re in a ``tmux`` session or not.

.. rubric:: Footnotes

.. [#] I’m especially impressed with ``tabbed``, as it feels somehow obvious
       yet magical.  A rare combination in my eyes.
.. [#] You’ll probably want a patch such as fancybar_ if you want to emulate
       the appearance of having a tab bar in ``dwm``.
.. [#] And using the window manager’s functionality means that ``vim`` session
       can be a ``gvim`` instance with nice colourful PNGs for signs_ instead
       of just characters too.
.. [#] You can find a quick patch to remove the daemon support and along with
       it the ``gtkhotkey`` dependency here_.

.. _tmux: https://tmux.github.io/
.. _tabbed: https://tools.suckless.org/tabbed
.. _xembed: https://standards.freedesktop.org/xembed-spec/xembed-spec-latest.html
.. _awesomewm: https://awesomewm.org/
.. _dwm: https://dwm.suckless.org/
.. _winwrangler: https://launchpad.net/winwrangler
.. _fancybar: http://dwm.suckless.org/patches/fancybar/
.. _xdotool: http://www.semicomplete.com/projects/xdotool/
.. _signs: http://vimdoc.sourceforge.net/htmldoc/sign.html
.. _here: https://github.com/JNRowe/jnrowe-misc/commit/a9249166b917110ecb69714ca08d8ff28870a9c7
