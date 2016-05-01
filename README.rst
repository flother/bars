A small command-line utility to take a CSV file and print a bar chart in
your terminal. Especially useful in combination with tools like CSVKit_,
q_, and jq_.

::

    $ curl -sL https://github.com/flother/bars/raw/master/tests/fixtures/us_region_pop.csv | \
      bars --label NAME \
           --value POPESTIMATE2015 \
           --width 72 \
           --domain 0 150000000 \
           -
    NAME             POPESTIMATE2015
    Northeast Region      56,283,891 ▓░░░░░░░░░░░░░░
    Midwest Region        67,907,403 ▓░░░░░░░░░░░░░░░░░
    South Region         121,182,847 ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    West Region           76,044,679 ▓░░░░░░░░░░░░░░░░░░░
                                     +---------+---------------------------+
                                     0    37,500,000             150,000,000

* Documentation: http://bars.readthedocs.io/
* Repository: https://github.com/flother/bars
* Issues: https://github.com/flother/bars/issues

Installation
------------

::

    pip install bars

Bars requires `Python 3`_, `Click`_, and `Agate`_.

Usage
-----

.. code-block:: text

    Usage: bars [OPTIONS] CSV

      Load CSV data and output a bar chart.

    Options:
      --label TEXT        Name or index of the column containing the label values.
                          Defaults to the first text column.
      --value TEXT        Name or index of the column containing the bar values.
                          Defaults to the first numeric column.
      --domain NUMBER...  Minimum and maximum values for the chart's x-axis.
      --width INTEGER     Width, in characters, to use to print the chart.
                          [default: 181]
      --skip INTEGER      Number of rows to skip.  [default: 0]
      --encoding TEXT     Character encoding of the CSV file.  [default: UTF-8]
      --no-header         Indicates the CSV file contains no header row.
      --use-ascii         Only use ASCII characters to draw the bar chart.
      --help              Show this message and exit.

Further details can be found in the documentation_.


.. _CSVKit: http://csvkit.readthedocs.org/en/latest/
.. _q: http://harelba.github.io/q/
.. _jq: https://stedolan.github.io/jq/
.. _Python 3: https://docs.python.org/3/
.. _Click: http://click.pocoo.org/6/
.. _Agate: http://agate.readthedocs.io/en/1.3.1/
.. _documentation: http://bars.readthedocs.io/
