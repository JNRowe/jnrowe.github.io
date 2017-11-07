:date: 2009-10-02
:tags: vim

Toggling settings in vim
========================

As you can never have enough keybinding tips and vim_ helps to prove that, the
tip for today answers Joshua’s question from ``##purplism``

    can you toggle settings in vim with a key?

The simple answer is yes, but how easy it is depends on what you’re trying to
toggle.  We need a state to test when toggling settings, so as long as we can
query the setting toggling it is easy.  For example, I have a binding in my
``~/.vimrc`` to toggle the value of background_.  As I use transparent terminals
the colours used for syntax highlighting can occasionally get a little difficult
to read depending on the wallpaper I’m using, the following function allows me
to quick toggle the ``background`` setting:

.. code-block:: vim

    " Map Shift-F12 to switch between light and dark
    function! Switch_background()
        if &background == "light"
            set background=dark
        else
            set background=light
        endif
    endfunction
    map <S-F12> :call Switch_background()<CR>

See :gist:`200255`

For some other commands such as toggling line numbering it can be much simpler:

.. code-block:: vim

    map <C-F12> :set number!<CR>

See :gist:`200257`

For those times when we can’t easily flip the setting on and off or query state
in a simple manner, the solution is to store state ourselves and test that.

We may, for example, wish to toggle a group of settings on or off at one time.
While we could test one of the settings in the toggle function it can become
quite brittle if we change those settings ourselves.  By storing our toggle
state in a variable we can test that instead.  The final — totally contrived
— example shows how to do that:

.. code-block:: vim

    " Map Mod1-F12 to toggle some vim goodness
    function! EditorvsNotepad()
        if g:notepad == "false"
            let g:notepad="true"
            syntax off
            set nohlsearch
            set laststatus=0
        else
            let g:notepad="false"
            syntax on
            set hlsearch
            set laststatus=2
        endif
    endfunction
    let g:notepad = "false"
    map <M-F12> :call EditorvsNotepad()<CR>

See :gist:`200258`

.. _vim: http://www.vim.org
.. _background: http://vimdoc.sourceforge.net/htmldoc/options.html#'background'
