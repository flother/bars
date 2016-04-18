Bars
====

Bars is a command-line utility that takes :abbr:`CSV (Comma-separated values)`
data and outputs a bar chart. It's especially useful in combination with tools
like CSVKit_ and jq_.

Let's say you want a chart of the ten most populous counties in the United
States. You could write something in your favourite programming language but
sometimes it's faster to work on the command-line::

    $ curl -s 'api.census.gov/data/2014/acs5?get=NAME,B01001_001E&for=county:*' | \
        jq -r '.[] | @csv' | \
        csvsort -c 2 -r | \
        head -n 11 | \
        bars --label NAME --value B01001_001E --width 72 -
    NAME                           B01001_001E
    Los Angeles County, California   9,974,203 ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    Cook County, Illinois            5,227,827 ▓░░░░░░░░░░░░░░░
    Harris County, Texas             4,269,608 ▓░░░░░░░░░░░░
    Maricopa County, Arizona         3,947,382 ▓░░░░░░░░░░░
    San Diego County, California     3,183,143 ▓░░░░░░░░░
    Orange County, California        3,086,331 ▓░░░░░░░░░
    Miami-Dade County, Florida       2,600,861 ▓░░░░░░░
    Kings County, New York           2,570,801 ▓░░░░░░░
    Dallas County, Texas             2,448,943 ▓░░░░░░░
    Queens County, New York          2,280,602 ▓░░░░░░
                                               +------+--------------------+
                                               0  2,500,000       10,000,000

In this short `Unix pipeline`_ we:

* get county populations as :abbr:`JSON (JavaScript Object Notation)` data from
  the :abbr:`US (United States)` Census Bureau;
* convert it to :abbr:`CSV (Comma-separated values)`;
* order the counties by population (largest first);
* keep only the first eleven rows (the header and ten data rows); and
* output that data as a bar chart.

The `source code can be found on GitHub`_. It's mostly a command-line wrapper
around the `Agate`_ library, which does the hard work in :class:`agate.Table`
and :meth:`agate.Table.print_bars`.

Installation
------------

Installing Bars system-wide is easy::

    sudo pip install bars

If you want to install the cutting-edge development version, use:

.. code-block:: text

    sudo pip install -e git+https://github.com/flother/bars#egg=bars

.. note::
   If you're familiar with virtualenv_ it's better to install Bars inside a
   virtual environment. If you do, use either of the previous commands but
   without the ``sudo``.

After you install Bars you'll have a new command-line utility, ``bars``. Pass
in a filename or use ``-`` for ``stdin``.

Tutorial
--------

Let's say you have a CSV file named ``us_pop.csv`` that contains the following
data:

======  ================  ===============  ===============
REGION  NAME              POPESTIMATE2014  POPESTIMATE2015
======  ================  ===============  ===============
1       Northeast Region  56171281         56283891
2       Midwest Region    67762069         67907403
3       South Region      119795010        121182847
4       West Region       75179041         76044679
======  ================  ===============  ===============

You want to make a bar chart showing 2015 population estimates for each region.
Bars makes this easy::

    $ bars --label NAME --value POPESTIMATE2015 us_pop.csv

Here we explicitly set a label (y-axis) and value (x-axis) but you don't have
to include them. Bars defaults to using the first text column for the label and
the first numeric column for the value. In the table above our label column,
``NAME``, is the first text column, and so we can leave the ``--label``
parameter out and still get the same result::

    $ bars --value POPESTIMATE2015 us_pop.csv

Our value column, ``POPESTIMATE2015``, is the third numeric column so we must
include it explicitly, but we can shorten it to just the column index (where
``1`` is the first column). ``POPESTIMATE2015`` is the fourth column so you can
use::

    $ bars --value 4 us_pop.csv

The bar chart defaults to the full width of your terminal, but you can set it
to a particular width using ``--width``::

    $ bars --value 4 --width 72 us_pop.csv

Now we have a bar chart that looks like this::

    NAME             POPESTIMATE2015
    Northeast Region      56,283,891 ▓░░░░░░░░░░░
    Midwest Region        67,907,403 ▓░░░░░░░░░░░░░
    South Region         121,182,847 ▓░░░░░░░░░░░░░░░░░░░░░░░
    West Region           76,044,679 ▓░░░░░░░░░░░░░░
                                     +---------+---------------------------+
                                     0    50,000,000             200,000,000

It looks nice, but perhaps there's too much of a margin to the right of the
bars. To change that we can set the *domain* for the x-axis --- that is, its
minimum and maximum values. Let's set the minimum to 0 and the maximum to 130
million::

    $ bars --value 4 --width 72 --domain 0 130000000 us_pop.csv
    NAME             POPESTIMATE2015
    Northeast Region      56,283,891 ▓░░░░░░░░░░░░░░░░
    Midwest Region        67,907,403 ▓░░░░░░░░░░░░░░░░░░░░
    South Region         121,182,847 ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    West Region           76,044,679 ▓░░░░░░░░░░░░░░░░░░░░░░
                                     +---------+---------------------------+
                                     0    32,500,000             130,000,000

You want to send the chart in an email to a friend, but you're worried the
Unicode characters that Bars uses will get mangled by their email client. Let's
print the chart using only ASCII::

    $ bars --value 4 --width 72 --domain 0 130000000 --use-ascii us_pop.csv
    NAME             POPESTIMATE2015
    Northeast Region      56,283,891 |::::::::::::::::
    Midwest Region        67,907,403 |::::::::::::::::::::
    South Region         121,182,847 |:::::::::::::::::::::::::::::::::::
    West Region           76,044,679 |::::::::::::::::::::::
                                     +---------+---------------------------+
                                     0    32,500,000             130,000,000


.. _CSVKit: http://csvkit.readthedocs.org/en/latest/
.. _jq: https://stedolan.github.io/jq/
.. _Unix pipeline: https://en.wikipedia.org/wiki/Pipeline_(Unix)
.. _source code can be found on GitHub: https://github.com/flother/bars
.. _Agate: http://agate.readthedocs.org/en/latest/
.. _virtualenv: https://virtualenv.pypa.io/
