Instant web server
==================

:date: 2009-10-12

Among the topics on our Linux list at work today was a question from Luke
Fletcher that I was expecting to unleash a flurry of emotional responses:

    What is the best small web server for testing site design and the like?

There were a couple of predictable rants about the benefits and drawbacks of
threading models.  Along with a couple of other topics entirely unhelpful for
the question at hand, but surprisingly little dissent over the choices.

Matt Traner's reply sums up the general feeling quite nicely:

    Just use whatever server you have installed already.  If you don't have
    *any* installed grab nginx_ as it works well and is quite small.

I agree with Matt's answer but I want to point a couple of possibly non-obvious
web servers that they, and you, are likely to have installed already.

Busybox
-------

All our Linux systems at the office include busybox_, and in the configuration
we use the httpd_ applet is built.  It is very lightweight, and incredibly
stable.  I often use it when testing or as a weak way to transfer files between
hosts when avahi_ isn't available or is too much hassle.  In my bash_
configuration I have a little functions to start up a ``busybox httpd`` server:

.. code-block:: bash

    http_serve()
    {
        if [ "${1}" = "--help" ]
        then
            echo "Usage:  ${FUNCNAME} [location]"
            echo "Start a httpd in \`location', defaulting to \`${http_serve_location}'."
            return 1
        fi
        busybox httpd -f -p 8080 -h ${1:-${http_serve_location}}
    }

`Fork this code <http://gist.github.com/208887>`__

``http_serve_location`` is set elsewhere in my configuration file, so that I can
keep per-machine settings separate.

Python
------

Python_ comes with its own basic web server, and it is very easy to use:

.. code-block:: text

    ~/Desktop/jnrowe.github.io/_site $ python2.6 -m SimpleHTTPServer 8080
    Serving HTTP on 0.0.0.0 port 8080 ...
    kate.localdomain - - [13/Oct/2009 01:16:51] "GET / HTTP/1.1" 200 -
    kate.localdomain - - [13/Oct/2009 01:16:51] "GET /css/content.css HTTP/1.1" 200 -
    kate.localdomain - - [13/Oct/2009 01:16:51] "GET /css/design.css HTTP/1.1" 200 -
    kate.localdomain - - [13/Oct/2009 01:16:51] "GET /css/pygments.css HTTP/1.1" 200 -
    kate.localdomain - - [13/Oct/2009 01:16:51] "GET /css/microformats.css HTTP/1.1" 200 -
    kate.localdomain - - [13/Oct/2009 01:16:51] "GET /css/print.css HTTP/1.1" 200 -
    kate.localdomain - - [13/Oct/2009 01:16:51] "GET /css/voice.css HTTP/1.1" 200 -
    ~/Desktop/jnrowe.github.io/_site $ python3.1 -m http.server 8080
    Serving HTTP on 0.0.0.0 port 8080 ...
    kate.localdomain - - [13/Oct/2009 01:17:23] "GET /2009/10/12/TaD-Instant_web_server.html HTTP/1.1" 200 -

Note that the name of the module has changed from ``SimpleHTTPServer`` to
``http.server`` for Python v3 and above.

I've specified the port 8080 to both calls in the snippet above, by default the
server port would be 8000.  If port 8000 is acceptable for you then you can save
yourself five keystrokes.

Ruby
----

ruby_ also comes with its own web server, one that you're probably already
familiar with if you're a rails_ user, called webrick_.  We need a little script
to use ``webrick``:

.. code-block:: ruby

    #! /usr/bin/ruby

    require "webrick"

    server = WEBrick::HTTPServer.new(
        :BindAddress => "localhost",
        :Port => 8080,
        :DocumentRoot => ARGV[0]
    )

    trap("INT") { server.shutdown }

    server.start

`Fork this code <http://gist.github.com/208891>`__

This script will serve files from whatever directory is specified as its first
argument.

Bonus
-----

Python also comes with a :abbr:`CGI (Common Gateway Interface)`-capable version called
``CGIHTTPServer`` and a :abbr:`XML (Extensible Markup Language)`-:abbr:`RPC (Remote Procedure Call)`
server called -- this shouldn't come as a surprise -- ``SimpleXMLRPCServer``.
They're very useful for testing out ideas and concepts without having to set
down lots of code.

.. _nginx: http://nginx.net/
.. _busybox: http://www.busybox.net/
.. _httpd: http://www.busybox.net/downloads/BusyBox.html#httpd
.. _avahi: http://avahi.org/
.. _bash: http://cnswww.cns.cwru.edu/~chet/bash/bashtop.html
.. _Python: http://www.python.org/
.. _ruby: http://www.ruby-lang.org/
.. _rails: http://www.rubyonrails.org/
.. _webrick: http://www.webrick.org/
