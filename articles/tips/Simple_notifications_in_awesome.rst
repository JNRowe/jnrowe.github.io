:date: 2009-10-04
:tags: awesome

Simple notifications in awesome
-------------------------------

.. highlight:: moon

On seeing my window notifications in awesome_ from a screencast for a new
project at work Matt Cooper asks:

    Is there a library that does those fancy notifications or do you have to
    hack it up yourself?

.. image:: /.static/2009-10-04-awesome_notifications.png
   :alt: notifications in awesome
   :align: right

There is a library to make notification popups in :command:`awesome`, and it is
called naughty_.  With it notifications are as simple as calling
``naughty.notify``, for example:

.. note::

    I use moonscript_ for all my lua_ needs, as it provides a nicer syntax and
    fixes some of the warts(such as global-by-default).  The examples below are
    all written in ``moonscript``.

::

    require "naughty"

    naughty.notify text: "my little popup", position: "bottom_left"

See :gist:`201130`

I do however define a few functions in my configuration file to simplify the
normal notifications I use::

    -- Generic info/warn/error notifications
    debug_messages = false
    notify =
        -- debug_notify: Display notification when debug_messages is true
        debug: (text) ->
            if debug_messages
                naughty.notify text: "<span color='#ff00ff'>Debug</span>: #{awful.util.escape text}",
                    timeout: 10, width:350,

        _gnotify: (ntype, text) ->
            colour = switch ntype
                when "info"
                    "#00ff00"
                when "warn"
                    "#ffff00"
                when "error"
                    "#ff0000"
                else
                    beautiful.fg_normal
            naughty.notify text: "<span color='#{colour}'>●</span> #{awful.util.escape text}",

        start: (text) ->
            notify._gnotify "info", text,
        stop: (text) ->
            notify._gnotify "error", text,
        warn: (text) ->
            notify._gnotify "warn", text,

See :gist:`201131`

.. note::
   If you’re willing to install lua-functional_, the above code snippet can be
   made much nicer by using its ``partial`` application support to define the
   final functions.

This group of functions, all namespaced under ``notify``, provide simple wrappers
for the everyday notifications I use.  ``notify.debug`` is a nice way to be able
to litter your configuration file with visible pointers as to what is going on,
set ``debug_messages = true`` in your ``rc.moon`` to enable all the debug
information and switch it back to ``false`` to stop it being displayed.

The ``notify.{start,stop,warn}`` functions prepend the text you pass it with
a coloured Unicode bullet.  awesome makes use of pango_
meaning you can easily use pretty much any character you wish, or more
specifically any character your font can display.  From time to time I’ve
experimented with using ``✔`` and ``✘``, but most of the fonts I prefer to use
don’t display them correctly(if you’re seeing two boxes your fonts don’t
either).

Window creation notifications
-----------------------------

One of the notifications I like to have is for when new windows are opened, this
way I don’t miss windows opening on tags I’m not currently viewing.

::

    awful.hooks.manage.register (startup) =>
        -- Display the window’s name, or just Application if it isn’t set
        notify.start "#{@name or 'Application'} started"

See :gist:`201132`

Network notifications
---------------------

I also have the following awful_ hook set to toggle my network monitor between
``lo`` and ``ppp0`` depending on whether my remote network interface is up.
Having the little popups to show when the network has gone down or come up is
quite nice, and definitely more noticeable than just changing the text in the
wibox_.  The code below changes the interface name in the ``wibox``, and
switches the network graph widget to use the appropriate input too.

::

    netiface = "lo"
    awful.hooks.timer.register 3, ->
        iface, state = if netiface == "lo" and io.open "/var/lock/LCK..ttyUSB0"
            "ppp0", "up"
        elseif netiface == "ppp0" and not io.open "/var/lock/LCK..ttyUSB0"
            "lo", "down"

        nettext_widget.text = " #{iface}:"
        wicked.register netbar_widget, "net", "${#{iface} up_b}", 3, "upload"
        wicked.register netbar_widget, "net", "${#{iface} down_b}", 3,
            "download"
        notify.start "PPP0 interface has come #{state}"

See :gist:`201133`

.. _awesome: http://awesome.naquadah.org/
.. _naughty: http://awesome.naquadah.org/doc/api/modules/naughty.html
.. _moonscript: https://github.com/leafo/moonscript/
.. _lua: http://www.lua.org/
.. _lua-functional: http://github.com/samsarin/lua-functional
.. _pango: http://www.pango.org/
.. _awful: http://awesome.naquadah.org/doc/api/modules/awful.hooks.html
.. _wibox: http://awesome.naquadah.org/doc/api/modules/wibox.html
