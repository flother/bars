#! /usr/bin/env python3
"""
Click-based command-line utility written in Python 3 that takes
:abbr:`CSV (Comma-separated values)` data and outputs a bar chart. The
heavy-lifting is done by :meth:`agate.Table.print_bars`.
"""
import io
import warnings

import agate
import click


class Number(click.ParamType):

    """
    Declares a parameter to be a numeric value. The value will be
    provided as an :class:`int` if the string is all numbers, else a
    :class:`float`.
    """

    name = "number"

    def __repr__(self):
        return self.name.upper().replace(" ", "_")

    def convert(self, value, param, ctx):
        """
        Converts the parameter value to an :class:`int` if the string is
        all numbers, else a :class:`float`. If conversion to a
        :class:`float` fails, an exception is raised.
        """
        if value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:
                self.fail("'{}' is not a valid number.".format(value))
        return value


def label_or_value_column_name(option_name, option_value, column_type, table):
    """
    Parses a ``--label`` or ``--value`` option value. Possibilities are
    that it's a string that matches a column name, that it's a column
    index (0 being the first column, -1 being the last), or that it's
    blank --- in which case the first column of type ``column_type`` is
    used, if there is one.

    Args:
        option_name: Name of the option (e.g. ``label`` for
            ``--label foo``).
        option_value: Option value given on the command-line (e.g.
            ``foo`` for ``--label foo``).
        column_type: If ``option_value`` is ``None`` then the name of
            the first column of this type (a sub-class of
            :class:`agate.DataType`) will be returned.
        table: :class:`agate.Table` instance.

    Returns:
        :class:`str`

    Raises:
        click.UsageError: ``option_value`` is ``None`` and a column of
            type ``column_type`` doesn't exist in ``table``.
        click.BadParameter: If an integer value is given and there is no
            column with that index (starting at one); or if a string is
            given and there is no column with that name.
    """
    try:
        option_value = int(option_value)
    except ValueError:
        pass

    if isinstance(option_value, int):
        # If the option value is an integer, use it as a column index.
        option_value = int(option_value)
        try:
            option_value = table.columns[option_value].name
        except IndexError:
            raise click.BadParameter("index {} is beyond the last column, "
                                     "'{}', at index {}".format(
                                        option_value, table.columns[-1].name,
                                        len(table.columns)))
    elif option_value is None:
        # If the option wasn't given on the command-line, find the first column
        # of type ``column_type``, if there is one.
        try:
            option_value = [c.name for c in table.columns
                            if isinstance(c.data_type, column_type)][0]
        except IndexError:
            raise click.UsageError("no --{} specified and no {} column "
                                   "found".format(option_name, column_type))
    else:
        # Use the option value as a column name.
        try:
            table.columns[option_value]
        except KeyError:
            raise click.BadParameter(
                "no column named '{}'".format(option_value),
                param_hint=option_name)
    return option_value


def label_column_name(value, table):
    """
    Parses a ``--label`` option value. For details see
    :func:`label_or_value_column_name`.

    Args:
        value: Option value given on the command-line (e.g. ``foo`` for
            ``--label foo``).
        table: :class:`agate.Table` instance.

    Returns:
        :class:`str`
    """
    return label_or_value_column_name("label", value, agate.Text, table)


def value_column_name(value, table):
    """
    Parses a ``--value`` option value. For details see
    :func:`label_or_value_column_name`.

    Args:
        value: Option value given on the command-line (e.g. ``bar`` for
            ``--value bar``).
        table: :class:`agate.Table` instance.

    Returns:
        :class:`str`
    """
    return label_or_value_column_name("value", value, agate.Number, table)


@click.command()
@click.option("--label", help="Name or index of the column containing the "
                              "label values. Defaults to the first text "
                              "column.")
@click.option("--value", help="Name or index of the column containing the bar "
                              "values. Defaults to the first numeric column.")
@click.option("--domain", help="Minimum and maximum values for the chart's "
                               "x-axis.", nargs=2, type=Number())
@click.option("--width", help="Width, in characters, to use to print the "
                              "chart.", default=click.get_terminal_size()[0],
                              show_default=True, type=click.INT)
@click.option("--skip", help="Number of rows to skip.", type=click.INT,
              default=0, show_default=True)
@click.option("--encoding", help="Character encoding of the CSV file.",
              default="UTF-8", show_default=True)
@click.option("--no-header", help="Indicates the CSV file contains no header "
                                  "row.", is_flag=True, default=False)
@click.option("--use-ascii", help="Only use ASCII characters to draw the bar "
                                  "chart.", is_flag=True, default=False)
@click.argument("csv", type=click.File("rt"))
def main(label, value, domain, width, skip, encoding, no_header, use_ascii,
         csv):
    """
    Load CSV data and output a bar chart.
    """
    # Ensure ``SIGPIPE`` doesn't throw an exception. This prevents the
    # ``[Errno 32] Broken pipe`` error you see when, e.g., piping to ``head``.
    # For details see http://bugs.python.org/issue1652.
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError):
        # Do nothing on platforms without signals or ``SIGPIPE``.
        pass

    # Load the CSV into an ``agate`` table. Catch warnings so a RuntimeError
    # doesn't get displayed when there are no column names (that is, when
    # ``header=False``).
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            table = agate.Table.from_csv(csv, skip_lines=skip,
                                         header=(not no_header),
                                         encoding=encoding)
        except UnicodeDecodeError:
            raise click.BadParameter("file not encoded as {}".format(encoding),
                                     param_hint="CSV")
        except ValueError:
            raise click.BadParameter("not a valid CSV file", param_hint="CSV")

    # Convert label and value into column names.
    label = label_column_name(label, table)
    value = value_column_name(value, table)

    with io.StringIO() as fh:
        table.print_bars(label, value, domain, width, fh, printable=use_ascii)
        fh.seek(0)
        click.echo(fh.read())


if __name__ == "__main__":
    main()
