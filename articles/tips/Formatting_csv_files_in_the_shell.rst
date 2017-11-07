:date: 2009-10-10
:tags: csv, unix

Formatting |CSV| files in the shell
===================================

kemi asks in ``#bash``:

    Are there any tools to format |CSV| files in the console?  Not
    interactive, no spreadsheets

column_, which on Linux is likely to be provided by util-linux_, does exactly
this.  The man page even offers an example of how it works(I've changed it
slightly to make it work correctly on my system):

.. code-block:: console

    $ (echo "PERM LINKS OWNER GROUP SIZE DATE HH:MM NAME";
    >     ls -l static/ | sed 1d) | column -t
    PERM        LINKS  OWNER  GROUP  SIZE   DATE        HH:MM  NAME
    -rw-r--r--  1      jay    jay    328    2009-09-25  02:59  body_background.png
    -rw-r--r--  1      jay    jay    7234   2009-09-25  02:59  draft.png
    -rw-r--r--  1      jay    jay    6253   2009-09-25  02:59  extract-metadata.xsl
    -rw-r--r--  1      jay    jay    13143  2009-10-07  09:05  foaf.rdf
    -rw-r--r--  1      jay    jay    3580   2009-09-25  02:59  gpg.asc
    -rw-r--r--  1      jay    jay    7739   2009-09-25  02:59  icon.png
    -rw-r--r--  1      jay    jay    96     2009-09-25  02:59  meta_background.png
    -rw-r--r--  1      jay    jay    411    2009-09-29  11:39  remote.png

Given some other standard commands we can mangle that data in various ways at
the shell prompt too, for example we may wish to display the total size of all
the files.  Or, as in the output below, the total size of all the :abbr:`PNG
(Portable Network Graphics)` files in the directory.

.. code-block:: console

    $ (echo "PERM LINKS OWNER GROUP SIZE DATE HH:MM NAME"
    >     ls -l static/ | sed 1d) | column -t | awk '{print}
    >         /\.png/ {sum+=$5}
    >         END {print "Total size of PNG files:", sum}'
    PERM        LINKS  OWNER  GROUP  SIZE   DATE        HH:MM  NAME
    -rw-r--r--  1      jay    jay    328    2009-09-25  02:59  body_background.png
    -rw-r--r--  1      jay    jay    7234   2009-09-25  02:59  draft.png
    -rw-r--r--  1      jay    jay    6253   2009-09-25  02:59  extract-metadata.xsl
    -rw-r--r--  1      jay    jay    13143  2009-10-07  09:05  foaf.rdf
    -rw-r--r--  1      jay    jay    3580   2009-09-25  02:59  gpg.asc
    -rw-r--r--  1      jay    jay    7739   2009-09-25  02:59  icon.png
    -rw-r--r--  1      jay    jay    96     2009-09-25  02:59  meta_background.png
    -rw-r--r--  1      jay    jay    411    2009-09-29  11:39  remote.png
    Total size of PNG files: 15808

In the original question on how to process |CSV| files all we really need to
do is get the data in to a state for ``column`` to process, and we can use
tr_ to do that.  An example using a small chunk of the network log on this
computer that we wish to format and calculate totals for could be:

.. code-block:: console

    $ cat stats
    2009-07-15T05:09:42+0100,16803,4304661,129262665
    2009-07-16T04:10:29+0100,17551,4012917,67572304
    2009-07-16T19:03:00+0100,17621,1712073,34162500
    2009-07-17T14:18:19+0100,7961,1071313,26286593
    2009-07-17T18:23:40+0100,1867,308589,6057915
    2009-07-17T18:53:21+0100,1740,180197,2907388
    2009-07-17T19:00:03+0100,356,152917,928948
    2009-07-17T22:01:57+0100,6611,1159789,25562873
    2009-07-18T13:09:31+0100,1681,164663,2049315
    2009-07-18T13:24:04+0100,834,54025,662134
    $ (echo "Date,Duration,Sent,Received";  cat stats ) \
    >     | tr ',' ' ' | column -t | awk '{print}
    >         !/Date/ {sent+=$3; recv+=$4}
    >         END {print "\nTotal sent: "sent", Total received: "recv}'
    Date                      Duration  Sent     Received
    2009-07-15T05:09:42+0100  16803     4304661  129262665
    2009-07-16T04:10:29+0100  17551     4012917  67572304
    2009-07-16T19:03:00+0100  17621     1712073  34162500
    2009-07-17T14:18:19+0100  7961      1071313  26286593
    2009-07-17T18:23:40+0100  1867      308589   6057915
    2009-07-17T18:53:21+0100  1740      180197   2907388
    2009-07-17T19:00:03+0100  356       152917   928948
    2009-07-17T22:01:57+0100  6611      1159789  25562873
    2009-07-18T13:09:31+0100  1681      164663   2049315
    2009-07-18T13:24:04+0100  834       54025    662134

    Total sent: 13121144, Total received: 295452635

.. |CSV| replace:: :abbr:`CSV (Comma Separated Values)`

.. _column: http://www.linuxmanpages.com/man1/column.1.php
.. _util-linux: http://www.kernel.org/pub/linux/utils/util-linux-ng/
.. _tr: http://www.linuxmanpages.com/man1/tr.1.php
