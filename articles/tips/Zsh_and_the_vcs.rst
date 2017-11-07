:date: 2009-10-28
:tags: git, vcs, zsh

Zsh and the |VCS|
=================

.. image:: /.static/2009-10-28-git_prompt.png
   :alt: Git prompt screenshot
   :align: right

I’ve recently switched to Zsh_ as my login shell after
9 years of using bash_, and for no particularly good reason either as they’re
both great interactive shells.  I guess all the *Kool Kids* are doing it, and
I’m just playing catchup.  The one side effect of that is I’m now scribbling
tips about ``Zsh`` too...

In a screenshot I posted in our bugtracker — that was considerably less staged
than the example above — one of my more visual hunks of ``Zsh`` configuration
was visible, leading to the following question from Dan Wilson:

    Okay, ‘fess time.  How do you get ``git`` branch names in the prompt?  How
    do you make the funky arrows show repo status?

Firstly, I use oh-my-zsh_ which is an excellent basis for ``Zsh`` configuration
files.  My prompt settings work within that framework, although they could be
converted to work with *plain* ``Zsh`` if you have the inclination.

If you want to see my entire “theme” file you can `clone my fork`_ and look at
`oh-my-zsh/themes/jnrowe.zsh-theme`_.

Branch names
------------

``Zsh`` comes with some neat |VCS| integration, that is exceptionally
documented_ in the manual.  I use that code to enable branch names in my
prompt, I use it directly instead of the code in ``oh-my-zsh`` that handles
``git`` status because it doesn’t do what I want [yet].  I use a format that
matches the default(``robbyrussell``) theme in ``oh-my-zsh``.

.. code-block:: zsh

    autoload -Uz vcs_info

    # See the documentation for the format string definition
    # This generates a fancy coloured string with $vcs:($branch)
    zstyle ':vcs_info:*' formats '%F{2}%s%F{7}:%F{2}(%F{1}%b%F{2})%f '
    zstyle ':vcs_info:*' enable git

See :gist:`220796`

Once we’ve configured ``vcs_info`` we just need to include
``${vcs_info_msg_0_}`` somewhere in our prompt to display the |VCS| and
current branch name.

``vcs_info`` works quite well, and supports many different systems(both common
and uncommon).  As the code snippet shows I enable support for git_ exclusively.
I’ve used it with mercurial_ too, and it works well.  darcs_ also appears to
work well, but it isn’t a system I use often enough to have tested it
thoroughly.

I tested ``bzr`` support while writing this but it is totally unusable because of
just how painfully slow ``bzr`` is.  On my system it adds close to one and half
seconds to every prompt display, although that could be improved if I wasn’t
using conservative CPU scaling to save power.  As a comparison the ``git`` info
takes less than a tenth of a second to calculate on the same system, and
``mercurial`` around three times that which is most definitely still usable.

.. note::
   There is a ``use-simple`` setting for the ``bzr`` support that may make the
   ``vcs_info`` functionality faster for you, albeit not noticeably on my system.
   It is also the only |VCS| that has such a hack, which is quite telling in
   itself.

Repository state
----------------

The “funky arrows” Dan asks about are dependent on the state of the current
working directory as can be seen in the screenshot at the top of this page.

+------------+----------------------------------------+
| Identifier | Description                            |
+============+========================================+
| white →    | Not a ``git`` repository               |
+------------+----------------------------------------+
| green ▶    | Clean ``git`` repository               |
+------------+----------------------------------------+
| red ▶      | Staged changes in ``git`` repository   |
+------------+----------------------------------------+
| yellow ▶   | Unstaged changes in ``git`` repository |
+------------+----------------------------------------+

Using these visual markers it is always obvious what state a directory is in,
I’ve toyed with adding more but suspect the lack of complexity is what makes
them so useful.

To enable them we need to add a `precmd hook`_ to calculate the repository
status:

.. code-block:: zsh

    autoload -U add-zsh-hook
    add-zsh-hook precmd prompt_jnrowe_precmd

    prompt_jnrowe_precmd () {
        vcs_info

        if [ -z "${vcs_info_msg_0_}" ]; then
            dir_status="%F{2}→%f"
        elif [[ -n "$(git diff --cached --name-status 2>/dev/null )" ]]; then
            dir_status="%F{1}▶%f"
        elif [[ -n "$(git diff --name-status 2>/dev/null )" ]]; then
            dir_status="%F{3}▶%f"
        else
            dir_status="%F{2}▶%f"
        fi
    }

See :gist:`220829`

With this added the we just need to include ``$dir_status`` in our prompt and the
status identifiers will be used.

If you are using a font which doesn’t display the characters correctly, either
change the characters in the ``dir_status`` values or switch to a `better font`_
that can display them.

.. _Zsh: http://www.zsh.org/
.. _bash: http://cnswww.cns.cwru.edu/~chet/bash/bashtop.html
.. _oh-my-zsh: http://github.com/robbyrussell/oh-my-zsh
.. _clone my fork: http://github.com/JNRowe/oh-my-zsh
.. _oh-my-zsh/themes/jnrowe.zsh-theme: http://github.com/JNRowe/oh-my-zsh/blob/master/themes/jnrowe.zsh-theme
.. _documented: http://zsh.sourceforge.net/Doc/Release/User-Contributions.html#SEC273
.. _git: http://www.git-scm.com/
.. _mercurial: http://www.selenic.com/mercurial/
.. _darcs: http://darcs.net
.. _precmd hook: http://zsh.sourceforge.net/Doc/Release/Functions.html#SEC45
.. _better font: http://www.is-vn.bg/hamster/
