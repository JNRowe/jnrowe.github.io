.. post:: 2018-11-05
   :tags: emacs, vim, evil

Evil Emacs steals my heart
==========================

*Many* of my co-workers use emacs_, it is probably the most popular editor on
our team and I understand why.

.. image:: /.images/standoff.png
   :alt: Editor icons
   :align: right

I was an ``emacs`` user — via MicroEMACS_ and later `GNU Emacs`_ — for many
years but at some point I switched to vim_.  I can’t even remember the exact
catalyst for change, but I am pretty fickle so it may not have even been all
that important.

Lately, I’ve found myself diving back in to ``emacs``.  In large part this is
because of evil_; I can be *in* ``emacs``, but *live* ``vim``.

Evil isn’t always evil
----------------------

So, ``evil-mode`` *is* awesome.

The kindest thing I can think to say about it is this: You’ll be angry when it
doesn’t work

This isn’t because it often breaks, quite the contrary.  It is simply because
it feels largely seamless.  I’ll give an example that mimics a recent session
to make my point.  For example, you’re hovering over a number you need to
change:

.. code-block:: c

    int magic_const = 974;

In ``vim``, you can execute :kbd:`ciw<C-r>=@"/2<CR>` to cleave the number.  The
command itself is saying:

:kbd:`ciw`
    Change the word my cursor is on(:kbd:`c`\hange :kbd:`i`\nner :kbd:`w`\ord)
:kbd:`<C-r>=`
    Insert the result of an expression(see ``:h i_CTRL-R_=`` for awesomeness)
:kbd:`@"`
    Use the text from last filled register, ie the text we just marked to be
    changed
:kbd:`/2`
    Half it
:kbd:`<CR>`
    Wow.

.. code-block:: c

    int magic_const = 487;

Whilst performing the same task thing in ``evil-mode`` I receive an error.
Emacs — quite rightly — expects you to write an elisp_ expression.  There is
nothing wrong with this, but it is a sign of how good ``evil-mode`` is.  It is
literally *so* good I forget I’m not using ``vim``.

Oftentimes a tool’s ``vim`` emulation can be summed up as needing to press
a key that kind of matches what something in ``vim`` might be, assuming you
didn’t really know what the key might be or when you’d use it.  Be that
sublimetext_’s ``vintage`` package that isn’t much more than normal and insert
mode, or elogv_’s bindings that mean you have to issue :kbd:`dd` to kill an
entry.  Frankly, many of the emulation layers often feel like you’re just
doubling the number of keys you have to press without any benefits [#]_.

Quirking the quirky
-------------------

.. image:: /.images/evil_emacs.png
   :alt: Emacs screenshot
   :align: right
   :scale: 50%

I’ll freely admit I’ve ``vim``\ified my ``emacs``.  I use evil_, my mode line
uses powerline_ to match vim-airline_.  I have ``zap-up-to-char`` mapped so
that I can mimic :kbd:`dt` when ``evil-mode`` is disabled.

Screenshots for ``emacs`` and ``vim`` really aren’t all that useful, because it
is the workflow that makes these tools powerful… but, above is my current
``emacs`` and below is my current ``vim``.

.. image:: /.images/delinquent_vim.png
   :alt: vim screenshot
   :align: left
   :scale: 50%

The big thing you’ll notice is the fonts.  In ``emacs`` I’m using scaled text
for headings in reST_ files.  I’m close to believing that headings,
proportional fonts for comments and the occasional inline image are enough to
switch to ``emacs``.

.. image:: /.images/misfeasant_emacs.png
   :alt: Inline images in Emacs
   :align: right
   :scale: 50%

In the third image you can see ``emacs`` is *displaying* the ``emacs``
screenshot in the buffer for *this* post.  This example may be quite pointless
[#]_, but it can be nice to have graphviz_ output class hierarchies in to
a buffer or database schema popups(like below).

.. image:: /.images/immoral_model.png
   :alt: Schema diagram
   :align: left
   :scale: 50%

Walking the branches
--------------------

I’ve decided to really dig in this time, not just switch on a whim.  I’m using
``emacs`` and *only* ``emacs`` for a month, followed by ``vim`` and *only*
``vim`` for a month.  I’m busily writing a document of bugbears about both
[#]_, and then figuring out which I want to fully invest in to.  I need to stop
flip-flopping.

I will say that there isn’t much in it.  With a converging setup there are
fewer and fewer differences to care about.  Things like the expression register
usage above, or built-in versus external HTML preview for documents like this.

I’m actually wondering whether a neovim_ client *in* a ``emacs`` frame would be
the golden option.  If you know of such a thing or a better option, drop me
a mail_!

.. rubric:: Footnotes

.. [#] elogv_ for Gentoo is probably the worst example of this, as :kbd:`d`
       *almost* works like ``vim`` but nothing does.
.. [#] Okay, completely pointless.
.. [#] org-mode_ and vim-orgmode_ allows me to keep this across editors.  There
       is very little point publishing it, as it can be summed up as “James
       pressed :kbd:`<C-x>$something` and was surprised.”

.. _emacs: https://www.gnu.org/software/emacs/
.. _MicroEMACS: ftp://ftp.cs.helsinki.fi/pub/Software/Local/uEmacs-PK/
.. _GNU emacs: https://www.gnu.org/software/emacs/
.. _vim: https://vim.sourceforge.io/
.. _evil: https://github.com/emacs-evil/evil
.. _sublimetext: https://www.sublimetext.com
.. _elisp: https://en.m.wikipedia.org/wiki/Elisp
.. _powerline: http://github.com/milkypostman/powerline/
.. _vim-airline: https://github.com/vim-airline/vim-airline
.. _reST: http://docutils.sourceforge.net/docs/user/rst/
.. _graphviz: https://www.graphviz.org/
.. _elogv: https://github.com/gentoo/elogv
.. _org-mode: https://www.orgmode.org/
.. _vim-orgmode: https://github.com/jceb/vim-orgmode
.. _neovim: https://neovim.io
.. _mail: jnrowe@gmail.com
