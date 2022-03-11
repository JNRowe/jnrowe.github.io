.. post:: 2019-04-05
   :tags: gps,time,bugs
   :image: 1

GPS rollover 2019
=================

Tomorrow we’re going to experience the simultaneously cataclysmic and mundane
consequences of a |GPS| rollover event.  *Many* things will break, *many* will
continue to work and *many* will just take a step closer to breaking… the fun
of date handling never ends.

.. image:: /.images/gps_calendar.png
   :alt: Pick a year, win a prize
   :align: right

.. note::

    This is an informal piece, not an official support channel.  If you use
    hardware I’m involved in building then contact your support channel, they
    are there to help.

What is the issue?
------------------

Since 1981 |GPS| signals have included a week number, which is provided as
a 10-bit field and as such can only store 1024 values(around 19.5 years).
Every time we hit that limit the week number rolls back to zero, and things may
fail to work correctly following that.

.. sidebar:: Prior to ‘81

    As a side note very early |GPS| transmissions didn’t even include week
    numbers in the signal.  Time was represented simply as a value *within*
    a week, and not *belonging* to a week.  If you work in the industry you
    still occasionally come across implementations that work like this, or
    issues that are caused by this.

    There have been a surprising number of other largely backward compatible
    upgrades to the |GPS| signal over the approaching fifty years of its
    development.  Coupled with the out of band enhancements such as :abbr:`WAAS
    (Wide Area Augmentation System)`, the accuracy and uses of |GPS|-based
    systems have increased a tremendous amount.

This is the second operational rollover event, the first happened in August
1999.  We — that is developers of |GNSS|-using systems — *are* prepared for
this, but the level of preparedness is unfortunately not uniform or indicative
of how well we’re handling this.

Mitigations
-----------

As this problem is quite well understood there has been an awful lot of effort
put in to working around it, some quite simple and some quite interesting.

Stored offset
'''''''''''''

The gold standard is systems that could afford the addition of :abbr:`NVRAM
(Non-Volatile Random Access Memory)`.  If we have a storage medium then the
previous known week number is often used as a check against rollover.  If we
know an initial epoch number from manufacturing date, and can see the
changeover at *some* point than you *shouldn’t* experience errors from
a rollover.

The obvious drawback being if a system is dormant for twenty years, but that
isn’t likely to be a real problem.

Week number offset
''''''''''''''''''

One of the most common mechanisms for dealing with rollover has been to bind it
to the firmware running on the device.  You simply assume the week number is
relative to a value given in the firmware.  For example, if we have firmware
from 2010 we can:

1. Assume we’re not running in 1999 via a time machine
2. Know we can’t see week numbers prior to our 2010 release date
3. Accept the given week number as valid through to 1023
4. After rollover treat week number 0 through 540 as being an offset past 1023

This is a reasonable solution in many circumstances, and one that exists in
many products in the field.  It also hints at part of the problem with this
method, and that is that a significant number of systems that will present
problems at various stages of their lives.  In the above example our system
*should* work through the epoch change in 2019, but will likely fail in August
2029 without intervention as we’ll trip over *our* workaround with our own
rollover bug causing it to reset to 2010.

|GNSS| voting comparisons
'''''''''''''''''''''''''

Many modern receivers support multiple signals; |GPS|, GLONASS, Beidou, &c.
Given this we can use consensus building to validate information.  If one of
the inputs is providing time data that is years away from the others you can
simply exclude it.

.. tip::

    Often systems may have alternative time sources available such as a regular
    low quality :abbr:`RTC (Real Time Clock)`, these can also be used as a hint
    towards consensus building too.

Leap second heuristic
'''''''''''''''''''''

|GPS| time is not corrected for leap seconds and as such increasingly drifts
from |UTC| over the years.  However, the current offset from |UTC| is
transmitted, and it can be used as an heuristic to configure the device from.

For example, when the first epoch ended in 1999 there was a 13 second offset
against |UTC|.  The switch to the third epoch happens with an 18 second offset.
Keying the epoch number off of the leap second offset *should* be a reasonable
way to handle rollover [#]_.

Forthcoming leap second adjustments are also published, so we can know both
the current offset and the maximum date given that future dates must be in the
future.

.. note::

    Leap second information is only published within |GPS| almanac, and is not
    available immediately following a cold boot of a device.  Depending on
    circumstances the 12 minute wait to acquire the almanac data may not be an
    issue.

What should I do?
-----------------

First check with your system’s supplier, they *should* have information on what
mitigations they have in place and what effects you should see now or at other
times in the future.

The next step should be to *ignore* what they told you and run a signal
simulator to figure out what is actually happening.  Date handling bugs happen
in so many layers you should have a testing procedure in place regardless of
your trust in a supplier [#]_.

.. warning::

    Fully read the documentation for simulators and receivers as many devices
    require a deep reset to make use of a simulated signal.  The P3200 sitting
    on my desk requires a hardware switch to be toggled before it will do
    anything beyond report “spoofing detected” if it receives unexpected
    signals, with the exception of a :abbr:`TOFU (Trust On First Use)` event
    following a deep reset.

Should I set an alarm for November 2038?
----------------------------------------

Yes and no.

The next rollover will occur in 2038, but new message types that use a 13-bit
week number field are available and increasingly being used.  This enhancement
changes the cycle to nearly 157 years, so we can naïvely hope this shouldn’t be
an issue again.

However, there *will* be systems that are still in the field that were
developed prior to the upgrade and there *will* be systems that were designed
later that still use the old 10-bit field for their week data.

Like I said in the previous section make sure you’re testing these things as
they’ll catch you out at some point.  Maybe even in fun ways such as exciting
interactions between the fourth GPS epoch and the *other* `2038 problem`_ in
January of that same year.

.. rubric:: Footnotes

.. [#] We’re assuming the earth doesn’t suddenly speed up enough that we need
       to start issuing negative leap seconds.
.. [#] I’m *absolutely* including products worked on by myself and my
       co-workers(forgive me!) in this.  People make mistakes, systems fail and
       skies may fall; having a good testing infrastructure is a must.

.. |GNSS| replace:: :abbr:`GNSS (Global Navigation Satellite System)`
.. |GPS| replace:: :abbr:`GPS (Global Positioning System)`
.. |UTC| replace:: :abbr:`UTC (Coordinated Universal Time)`

.. _2038 problem: https://en.wikipedia.org/wiki/Y2038_problem

.. spelling::

    Beidou
