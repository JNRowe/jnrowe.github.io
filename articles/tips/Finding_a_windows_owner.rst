:date: 2009-10-06
:tags: X11

Finding a window's owner
========================

Rach Holmes asks on our Linux list:

    How do I find out what app keeps opening that annoying window in gnome?

Jack McIntyre made a couple of outstanding correct guesses, but predictably Rach
still wanted to know a generic solution and I offer this tip in response.

The easy way
------------

Many windows define a ``WM_COMMAND`` property that is set to the command name of
the application, if that exists all we have to do is read it:

.. code-block:: console

    $ xprop  | grep WM_COMMAND
    WM_COMMAND(STRING) = { "urxvt", "-cd", "/home/jay/Desktop" }

However, not all applications set this property.  Examples of applications that
don't set this property include firefox_ and gimp_.  In fact, many of the modern
applications you find on desktop systems don't set this property at all.

The other way
-------------

.. FIXME

EWMH_, the Extended Window Manager Hints standard, defines a property called
``_NET_WM_PID`` that, if defined, is the process id of the application that
opened the window.  We have a couple of options to access that property, my
favourite would be wmctrl_ and another would be xprop_ which is often installed
by default.

.. code-block:: console

    $ wmctrl -lp
    0x01200003  2 13398  kate 2009-10-06-TaD-Finding_a_windows_owner.textile [+] - gvim
    0x01000006  3 9992   kate Irssi: [JNR___@freenode] [#github]
    0x00c00005  1 10134  kate SpotMe - Opera
    0x00600019  0 9992   kate jay@kate:~/Desktop/jnrowe.github.io
    $ xprop | awk '/_NET_WM_PID/ {print $NF}'
    9992
    $ tr '\000'  ' ' < /proc/9992/cmdline
    /usr/bin/urxvtd -q -f -o

The ``wmctrl`` output has five aligned columns.  The first is the window id, the
second the desktop is visible on, the third is the process id, the fourth is the
client machine and the fifth is the window's title string.  And with the ``xprop``
example we must select a window with the mouse when calling ``xprop``, and then we
pluck the process id from the output.

The ``cmdline`` value for the process from procfs_ is finally read.  The ``tr``
command is needed because options are separated by null terminators.

The problems
------------

Back to the original question and Rach was looking for a way to stop the window
from showing up, the immediate response to the annoying window problem is to
find its process id and send it a ``SIGTERM``.  It seems like a reasonable idea,
but I've been choosing the ``urxvtd`` examples on purpose to prove a point.

``urxvtd`` is the terminal daemon provided by rxvt-unicode_, all terminals that
are spawned by it will have the same ``_NET_WM_PID`` value and ``WM_COMMAND``
string.  This isn't just an issue with ``urxvtd`` either, it happens with all
applications that operate in this way.  Sending a ``SIGTERM`` to every terminal
opened by ``urxvtd`` probably isn't what we would want to do, so you should
always think very carefully before sending terminate signals.

.. _firefox: http://www.mozilla.com/firefox
.. _gimp: http://www.gimp.org/
.. _EWMH: http://standards.freedesktop.org/wm-spec/wm-spec-1.3.html
.. _wmctrl: http://sweb.cz/tripie/utils/wmctrl/
.. _xprop: http://www.xfree86.org/current/xprop.1.html
.. _procfs: http://blogs.sun.com/eschrock/entry/the_power_of_proc
.. _rxvt-unicode: http://software.schmorp.de/
