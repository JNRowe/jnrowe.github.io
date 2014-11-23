Simple notifications in awesome
-------------------------------

:date: 2009-10-04

On seeing my window notifications in awesome_ from a screencast for a new
project at work Matt Cooper asks:

    Is there a library that does those fancy notifications or do you have to
    hack it up yourself?

.. image:: /.static/2009-10-04-awesome_notifications.png
   :alt: notifications in awesome
   :align: right

There is a library to make notification popups in awesome, and it is called
naughty_.  With it notifications are as simple as calling ``naughty.notify``,
for example:

.. code-block:: lua

    require("naughty")

    naughty.notify({ text="my little popup", position="bottom_left" })

`Fork this code <http://gist.github.com/201130>`__

I do however define a few functions in my configuration file to simplify the
normal notifications I use:

.. code-block:: lua

    -- Generic info/warn/error notifications
    notify = {}

    local debug_messages = false
    -- debug_notify: Display notification when debug_messages is true
    function notify.debug(text)
        if debug_messages then
            naughty.notify({ text="<span color='#ff00ff'>Debug</span>:" .. awful.util.escape(text),
                            timeout=10, width=350 })
        end
    end

    function notify._gnotify(ntype, text)
        local colour = beautiful.fg_normal
        if ntype == "info" then
            colour = "#00ff00"
        elseif ntype == "warn" then
            colour = "#ffff00"
        elseif ntype == "error" then
            colour = "#ff0000"
        end
        naughty.notify({ text="<span color='" .. colour .. "'>●</span> " ..
                            awful.util.escape(text) })
    end

    function notify.start(text)
        notify._gnotify("info", text)
    end
    function notify.stop(text)
        notify._gnotify("error", text)
    end
    function notify.warn(text)
        notify._gnotify("warn", text)
    end

`Fork this code <http://gist.github.com/201131>`__

.. note::
   If you're willing to install lua-functional_, the above code snippet can be
   made much nicer by using its ``partial`` application support to define
   ``start`` and ``stop``.

This group of functions, all namespaced under ``notify``, provide simple wrappers
for the everyday notifications I use.  ``notify.debug`` is a nice way to be able
to litter your configuration file with visible pointers as to what is going on,
set ``debug_messages = true`` in your ``rc.lua`` to enable all the debug information
and switch it back to ``false`` to stop it being displayed.

The ``notify.{start,stop,warn}`` functions prepend the text you pass it with
a coloured Unicode bullet.  awesome makes use of pango_
meaning you can easily use pretty much any character you wish, or more
specifically any character your font can display.  From time to time I've
experimented with using ``✔`` and ``✘``, but most of the fonts I prefer to use
don't display them correctly(if you're seeing two boxes your fonts don't
either).

Window creation notifications
-----------------------------

One of the notifications I like to have is for when new windows are opened, this
way I don't miss windows opening on tags I'm not currently viewing.

.. code-block:: lua

    awful.hooks.manage.register(function (c, startup)
        -- Display the window's name, or just Application if it isn't set
        notify.start((c.name or "Application") .. " started")
    end)

`Fork this code <http://gist.github.com/201132>`__

Network notifications
---------------------

I also have the following awful_ hook set to toggle my network monitor between
``lo`` and ``ppp0`` depending on whether my remote network interface is up.
Having the little popups to show when the network has gone down or come up is
quite nice, and definitely more noticeable than just changing the text in the
wibox_.  The code below changes the interface name in the ``wibox``, and
switches the network graph widget to use the appropriate input too.

.. code-block:: lua

    awful.hooks.timer.register(3, function ()
        if netiface == "lo" and io.open("/var/lock/LCK..ttyUSB0") then
            netiface = "ppp0"
            nettext_widget.text = " ppp0:"
            wicked.register(netbar_widget, "net",
                "${ppp0 up_b}",
                3, "upload")
            wicked.register(netbar_widget, "net",
                "${ppp0 down_b}",
                3, "download")
            notify.start("PPP0 interface has come up")
        elseif netiface == "ppp0" and not io.open("/var/lock/LCK..ttyUSB0") then
            netiface = "lo"
            nettext_widget.text = " lo:"
            wicked.register(netbar_widget, "net",
                "${lo up_b}",
                3, "upload")
            wicked.register(netbar_widget, "net",
                "${lo down_b}",
                3, "download")
            notify.stop("PPP0 interface has gone down")
        end
    end)

`Fork this code <http://gist.github.com/201133>`__

.. _awesome: http://awesome.naquadah.org/
.. _naughty: http://awesome.naquadah.org/doc/api/modules/naughty.html
.. _lua-functional: http://github.com/samsarin/lua-functional
.. _pango: http://www.pango.org/
.. _awful: http://awesome.naquadah.org/doc/api/modules/awful.hooks.html
.. _wibox: http://awesome.naquadah.org/doc/api/modules/wibox.html
