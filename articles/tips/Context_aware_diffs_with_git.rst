:date: 2009-09-29
:tags: git

Context aware diffs with git
============================

Earlier this week Luke Cox asked in response to a patch I sent:

    What version of git_ are you using?  Mine doesn’t seem to produce the right
    location output for :command:`format-patch`.

:command:`git`, by default, displays a `function name in the hunk header`_ of
its :command:`diff` output.  It produces some really nice output for certain
languages, but out of the box it doesn’t display nice information for all the
file formats you may use.

.. code-block:: diff

    diff --git 1/config/dconf/user.ini 2/config/dconf/user.ini
    index d4bf8a0..5559f9f 100644
    --- 1/config/dconf/user.ini
    +++ 2/config/dconf/user.ini
    @@ -5,5 +5,5 @@ org/gtk/settings/file-chooser
     sort-column='name'
     show-size-column=true
     startup-mode='cwd'
    -show-hidden=false
    +show-hidden=true
     sort-directories-first=true

The patch I sent Luke included a significant change to an `.ini`_ format file,
including some mostly accurate location information in the hunk header as in
the example above.  It wasn’t because I use a newer version of :command:`git`,
just that I’ve set it up to use different matchers for different files.  In my
:file:`~/.config/git/config` I have the following snippet to use better
function names in ``ini`` and ``adr`` files:

.. code-block:: ini

    [diff "ini"]
        funcname = "^\\[\\(.*\\)\\]$"
    [diff "adr"]
        funcname = "^#.*$"

.. warning::

    Be sure to escape backslashes, as the config parser will eat a single
    backslash before it is even seen by the diff driver.  For the full details
    on the format, see :manpage:`gitattributes(7)`.

And, to enable them you must tell :command:`git` which files to use the new
matchers with by editing the :file:`.gitattributes` file:

.. code-block:: text

    *.ini diff=ini
    *.adr diff=adr

The ``funcname`` values are simple |RegEX| to search for, so in the ``ini``
example it is searching for a line that begins with a :regexp:`[` and ends with
a :regexp:`]` as these are the common section headers.  And the ``adr`` matcher
just specifies a line that begins with a :regexp:`#`.

It is important to match the entire string or to use grouping, as it is the
matched content that is used in the diff hunk’s output.  As can be seen in the
``ini`` example, I group only the text between ``[`` and ``]`` so that the
brackets aren’t included in the header.

.. _git: http://www.git-scm.com/
.. _function name in the hunk header: http://www.gnu.org/software/diffutils/manual/html_node/C-Function-Headings.html
.. _.ini: http://www.cloanto.com/specs/ini.html
