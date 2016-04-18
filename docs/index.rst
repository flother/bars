Bars
====

Bars is a command-line utility that takes :abbr:`CSV (Comma-separated values)`
data and outputs a bar chart. It's especially useful in combination with tools
like CSVKit_ and jq_.

Let's say you want a chart of the ten most populous counties in the United
States. You could write something in your favourite programming language but
sometimes it's easier to just work on the command-line::

    $ curl -s 'api.census.gov/data/2014/acs5?get=NAME,B01001_001E&for=county:*' | \
        jq -r '.[][0:2] | @csv' | \
        csvsort -c 2 -r | \
        head -n 11 | \
        bars --width 72 -
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
* pass it through a jq filter to keep only county names and populations, and
  convert it to :abbr:`CSV (Comma-separated values)`;
* order the counties by population (largest first);
* keep only the first eleven rows (the header and ten data rows); and
* output that data as a bar chart.

The `source code can be found on GitHub`_. It's mostly a command-line wrapper
around the `Agate`_ library, which does the hard work in :class:`agate.Table`
and :meth:`agate.Table.print_bars`.

Installation
------------

::

    pip install bars

Once installed you have a new command-line utility, ``bars``. Pass in a
filename or use ``-`` for ``stdin``.

Usage
-----

.. code-block:: text

    Usage: bars [OPTIONS] CSV
    
      Load a CSV file and output a bar chart.
    
    Options:
      --label TEXT        Name or index of the column containing the label values.
                          Defaults to the first text column.
      --value TEXT        Name or index of the column containing the bar values.
                          Defaults to the first numeric column.
      --domain NUMBER...  Minimum and maximum values for the chart's x-axis.
      --width INTEGER     Width, in characters, to use to print the chart.
                          [default: 80]
      --skip INTEGER      Number of rows to skip.  [default: 0]
      --encoding TEXT     Character encoding of the CSV file.  [default: UTF-8]
      --no-header         Indicates the CSV file contains no header row.
      --use-ascii         Only use ASCII characters to draw the bar chart.
      --help              Show this message and exit.

.. _CSVKit: http://csvkit.readthedocs.org/en/latest/
.. _jq: https://stedolan.github.io/jq/
.. _Unix pipeline: https://en.wikipedia.org/wiki/Pipeline_(Unix)
.. _source code can be found on GitHub: https://github.com/flother/bars
.. _Agate: http://agate.readthedocs.org/en/latest/
