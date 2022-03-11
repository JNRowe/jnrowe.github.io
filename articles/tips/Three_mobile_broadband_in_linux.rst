.. post:: 2009-10-14
   :tags: linux, three

Three mobile broadband in Linux
===============================

.. highlight:: text

Steve Lowry is picking up his Three_ modem this afternoon and asks on our
internal Linux list if it supports Linux.

    I’ve ordered the Huawei E220 as it was free.  Is it likely to work with
    Linux?  And, if so what should I be looking for to set it up?

I’ve had a Huawei |USB| modem for about six months now and it works fine in
Linux, although it is probably a slightly different model.  The box and case
for mine claims it is a E160G, whereas :command:`lsusb` from usbutils_ claims
it is a E220.  The manufacturers of these types of products routinely change
the components and models without updating the product codes, so you’ll have to
wait until you plug it in to see what model it actually is.

As for how to make it work?  Simply use a distribution that comes with
NetworkManager_ and NetworkManager’s `mobile broadband provider database`_.
When I tested it on a friend’s install with that setup last month it worked out
of the box, all you had to do was plug it in and select the network.

The route to fail
-----------------

If, like me, you’d prefer not to install NetworkManager you can manually
configure the device using pppd_, and life is even easier now than it was when
I did it as there is plenty more information available(including this I guess).

Finding the |APN|
'''''''''''''''''

The first thing you need is your provider’s |APN|, and the easiest place to
find it is from the `NetworkManager database`_.  If yours is not there you’ll
have to dig further.  When I originally got my device that database was
practically empty, so I had to resort to other means to find the |APN|.

We can extract the |APN| from the Windows driver that came with the device.
The driver can be found on the device itself because it also acts a small
:abbr:`SCSI (Small Computer Systems Interface)` device with a filesystem.  It
is actually pretty clever, assuming it works as advertised, as it can
self-install its own driver when plugged in.

If we find the device name with :command:`dmesg` we can mount it, and pull the
|APN| from the Windows driver:

.. code-block:: bash

    mkdir e220_drivers; cd e220_drivers
    mount -t vfat /dev/sr2 /mnt/huawei
    for file in /mnt/huawei/**/*.cab; do unpack $file; done

The :command:`unpack` tool from above is just a wrapper around common
archivers, and the tool you actually need to extract the ``cab`` files is
unshield_.  Contrary to my first idea cabextract_ doesn’t work, as these files
are actually made by ``installshield``.

With the |APN| in hand all we need to do now is configure our system.

Kernel
''''''

If you’re using a vendor supplied kernel the options we need are hopefully
already enabled.  If they’re not, or you build your own kernels, there are few
changes we need to make to the kernel configuration.

The dongle itself needs ``CONFIG_USB_SERIAL_OPTION`` enabled, which is labelled
as ``USB driver for GSM and CDMA modems`` in the kernel’s ``menuconfig``.  It
can be found hidden away under the “USB Serial Converters” section in 2.6.31.

We also need ``CONFIG_PPP`` and ``CONFIG_PPP_ASYNC`` support, which can be
found in the “Network devices” section of the config.  Unlike the old-style
dialup you may be used to use there is no point enabling the :abbr:`PPP
(Point-to-Point Protocol)` compression options as they are not supported by
mobile providers in general, partly because the data is already compressed.

Then just rebuild the kernel, and check that the dongle shows up in
:command:`dmesg` output when it is plugged in.  If it does we’re ready for the
next step.

/etc/chatscripts/three
''''''''''''''''''''''

We need a :command:`pppd` chatscript for the connection, the format and
settings of this file can be found in the :manpage:`chat(8)` manpage.  My
chatscript is below::

    TIMEOUT 3
    ECHO ON
    ABORT 'BUSY'
    ABORT 'DELAYED'
    ABORT 'ERROR'
    ABORT 'NO ANSWER'
    ABORT 'NO CARRIER'
    ABORT 'NO DIALTONE'
    ABORT 'VOICE'
    '' \rAT
    OK 'AT+CGDCONT=1,"IP","3internet"'
    OK ATD*99#
    CONNECT ""

Exchange ``3internet`` for your |APN| in the example above, if it differs.

It is also possible, yet unlikely, that you’ll have to call a different number
to ``*99#``.  If this was the case you would have found that out from extracting
the data from the drivers or looking your network up in the NetworkManager
database.

Notice the very short value for timeout, I’ve come to that value empirically.
If the connection isn’t up after 3 seconds it is not coming up, and you’re just
wasting time before you retry.

/etc/ppp/peers/three
''''''''''''''''''''

We also need a peer script, and the format of that file is described in the
:manpage:`pppd(8)` manpage.  Mine can be used as an example::

    debug
    noauth
    connect "/usr/sbin/chat -v -f /etc/chatscripts/three"
    noipdefault
    usepeerdns
    /dev/ttyUSB0
    defaultroute
    persist
    crtscts
    lcp-echo-failure 0

You may have to change your device settings if the dongle doesn’t show up as
:file:`/dev/ttyUSB0`, but other than that the file should be correct.

Note that we don’t set a speed in our peer file, and this may appear unusual to
you if you’ve configured :command:`pppd` manually in the past.  The reason is
that interface speed for |USB| modems is set by the kernel, and adding a value
here is pointless.

passwords
'''''''''

We don’t need to add an entry to :file:`chap-secrets` or :file:`pap-secrets` as
authentication isn’t required, but if you’re following along having chosen to
use a configuration tool such as pppconfig_ just enter any values you wish as
they’re silently ignored.

I’m told the same applies to wvdial_, so if it complains about requiring
a password just add an empty or random string to stop the errors.

Testing the connection
''''''''''''''''''''''

To test the connection all we need to do is issue ``pon three``, or use the
graphical tool in your distro if you wish.  The first time you do this you
should watch the output of your syslog to look for errors, the errors can be
found in syslog because we supplied ``debug`` in our peer script.

On my system the log can be comfortably viewed with ``tail -f
/var/log/ppp/current``, but it is system dependent and if you don’t use metalog_
it will definitely be somewhere else in ``/var/log``.

If the connection worked fine that is all there is to it, now just enable the
connection at system startup or configure udev_ to connect when the device is
inserted if it will not always be connected.

.. note::
   These devices can take anywhere between ten and thirty seconds to “settle”
   once plugged in. So, don’t block on this service if you add it to the system
   startup scripts as it can significantly slow down the system boot time.  On
   my dongle you can visually check how long the device takes to settle by
   watching the :abbr:`LED (Light Emitting Diode)` on the case, when it changes
   from green it has found a network signal and is ready to use.

If the connection didn’t work correctly look at the debugging output in syslog
and check the :command:`pppd` manual page to look up the error codes.

Happy, erm… mobility.

.. |APN| replace:: :abbr:`APN (Access Point Name)`
.. |USB| replace:: :abbr:`USB (Universal Serial Bus)`

.. _Three: http://three.co.uk
.. _usbutils: http://linux-usb.sourceforge.net/
.. _NetworkManager: http://www.gnome.org/projects/NetworkManager/
.. _mobile broadband provider database: http://live.gnome.org/NetworkManager/MobileBroadband/ServiceProviders
.. _pppd: http://www.samba.org/ppp
.. _NetworkManager database: http://live.gnome.org/NetworkManager/MobileBroadband/ServiceProviders
.. _unshield: http://synce.sourceforge.net/synce/unshield.php
.. _cabextract: http://www.cabextract.org.uk/
.. _pppconfig: http://http.us.debian.org/debian/pool/main/p/pppconfig/
.. _wvdial: http://alumnit.ca/wiki/?WvDial
.. _metalog: http://metalog.sourceforge.net/
.. _udev: http://www.kernel.org/pub/linux/utils/kernel/hotplug/udev.html

.. spelling::

    syslog
