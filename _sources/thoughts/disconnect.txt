:tags: focus, denoise, net
:date: 2014-09-18

Cleanse thy soul
================

For the past few years I've taken to having routine breaks from certain
timesinks to help me focus and also to denoise some of my thoughts.  The number
one timesink in my world is without doubt the interwebs, and there are a few
steps I've taken to weaken its stranglehold.

Perhaps the following will help you, or perhaps you'll email_ me to point out
your ideas for me to try.

Cut the tether
--------------

I track every thing that I *practically* can, doing so can be very empowering.
This is something which the buzzwordy types apparently refer to as The
Quantified Self, and despite knowing that I continue to do so.

With a query of my network logs [#s1]_ I can tell you that for the first nine
months of this year I've been entirely without internet access for thirty-one
percent of the time.  Last year the final amount was thirty-eight percent, and
once our Winterval shutdown is included I'd expect this year to be about the
same.

It isn't just a case of being without internet access for a few hours or on
certain days either, my longest *complete* break this year was a straight
thirteen days back in May.

The number one thing I've learnt is that a lot of the things I burnt time on
were genuinely just burnt.  For example, news sites feel mostly pointless to
me at this point.

* Mainstream news is invariably a PR copy'n'paste fest, which is *really*
  noticeable when you come back from a break and catch up on various feeds in
  one huge chunk.
* Sites with a slightly more tech bias like HackerNews and its ilk are just
  a complete time hole.  Often the really interesting tech stories will bubble
  up elsewhere in a curated fashion(such as Trivium_), and for example on HN the
  majority of posts and comments are just US politics or occasionally
  interesting insights from the SV bubble anyway.

I'll still catch up from a couple of, in my opinion, trusted sources.  That is
to say I'll dip in to a few categories on BBC news and perhaps visit The
Guardian's site(although I do that considerably less over the past year
according to my data).  I also like to avail myself of a little `Russia Today`_
and `Al Jazeera`_ to keep the bias in check a touch.

With a simple rdial_ report I can also tell you that on an average internet
connected day I can spend an hour reading news, friend's blogs, sports stories,
&c.  A big chunk of that time is also combined with breakfast, so I choose to
let it slide for the most part.

Tighten the noose
-----------------

For the two-thirds of the year that I have internet access, I've started to
severely restrict access.

It all started with a friend who -- while wearing his tinfoil hat -- preached
about how we all need to consider blocking sites that use :abbr:`CDNs (Content
Delivery Network)` in much the same way that many of us block web analytics
companies.  We're probably giving up more tracking data to the large CDNs then
we do to the simple analytics companies.

The thought popped in to my mind that a whitelist, instead of a blacklist, might
actually be workable and since last November I've taken to doing just that.

The strangest result in my mind is just how short the list is.  My old advert
and analytics blacklist had close to 1500 entries, and would obviously miss many
"nasties" that I either hadn't seen or that were simply new.

The whitelist, on the other hand, has only ever had 900 entries. Right now it
has less than 150 thanks to the automated decay-based-on-visits purging of the
entries it contains.

The whitelist approach also feeds in to my data tracking habit, as I can now
tell from the decay tracking data when bursts of certain sites appear.  For
example, StackOverflow(and ``cdn.sstatic.net/stackoverflow/`` for styling) was
on the whitelist for two weeks in June with six visits, which happens to
coincide with a project that involved porting a tool to Windows.

The act of using a whitelist makes the point of procrastination noticeable and
adds a cost to even starting it.  Every time I want to visit a new site [#s2]_,
I have to highlight the URL and rattle a key combo in awesome_ that updates the
whitelist to enable access to it.

On the knoll
------------

I know the whole "go without the internet" thing is going to strike people as
unworkable.  Questions abound about contact via email, missing bug reports,
skipping meeting logs, depriving myself of invites to weddings I don't wish to
attend and so on.  I do realise it isn't achievable for everyone, but with
a little effort it should at the very least be achievable for one day a week.

The other advantage of doing so is the forced removal from services that
actively destroy your privacy and the privacy of your friends and family, which
is something that feels increasingly important in recent years.  For example,
I no longer actively store my addressbook online [#s3]_ nor do I use a service
to help me process receipts any more.

.. sidebar:: Admission of guilt

    I have to admit that I haven't quite dropped all the services I'd like to,
    here are a few:

    * Strava - I'm still kind of using for the time being, although Keith's
      replacement looks like it will fulfil my needs :abbr:`RSN (Real Soon
      Now™)`.
    * status.net - There are one or two people I don't want to lose contact with
      who aren't able to access our private server because of geo-filtering, and
      I don't know how that can be fixed.

There are a myriad of benefits to dropping the reliance on :abbr:`SaaS (Software
as a Service)` affairs.  The chance of any of them existing tomorrow is frankly
not all that great: shuttering, buy-out closures, "pivotting", &c.  You can
also retain some level of control over your own data, knowing that for example
it isn't being sold or stored in regions with little to no data protection
regulation.

In all honesty, I -- no, *we* -- should have resisted the urge to use so called
cloud services from the outset.  One doesn't need to be a fully paid up member
of the tinfoil hat brigade to know that it is just not acceptable to entrust
your important data to external companies for the sake of a little convenience
or a shiny interface.

Killing my internet access for chunks of time really pointed out how much I had
come to rely on services far beyond my control, and the freedom one feels when
you regain some of that is very comforting.

.. rubric:: Footnotes

.. [#s1] The code I use is an unreleased project created by a friend, but
   vnstat_ may work equally well for the same purpose.
.. [#s2] For the most part I whitelist based on hostname, but as in the
   StackOverflow styling example will whitelist specific paths on hosts on some
   occasions.
.. [#s3] I'm aware that Google has access to a small corner of my contacts graph
   via gmail, but I haven't yet decided how I plan to resolve.  I've never used
   gmail for work or mail that I'd be uncomfortable reading in public, but it
   does act as a nice sieve for everything else right now.

.. _email: jnrowe@gmail.com
.. _rdial: https://pypi.python.org/pypi/rdial/
.. _trivium: http://chneukirchen.org/trivium/
.. _Russia Today: http://rt.com/
.. _Al Jazeera: http://www.aljazeera.net/
.. _vnstat: http://humdi.net/vnstat/
.. _awesome: http://awesome.naquadah.org/

