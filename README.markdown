This is a Python implementation of ProPublica's [TableFu](http://propublica.github.com/table-fu/).
This API is similar, though following Python conventions.

Usage:

    >>> csv = open('tests/test.csv')
    >>> table = TableFu(csv)
    >>> table.columns
    ['Author', 'Best Book', 'Number of Pages', 'Style']

    # get all authors
    >>> table.values('Author')
    ['Samuel Beckett', 'James Joyce', 'Nicholson Baker', 'Vladimir Sorokin']

    # total a column
    >>> table.total('Number of Pages')
    1177.0


More documentation coming.
