This is a Python implementation of ProPublica's [TableFu](http://propublica.github.com/table-fu/).
This API is similar, though following Python conventions.

Usage:

    >>> from table_fu import TableFu
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
    
    # each TableFu instance acts like a list of rows
    >>> table[0]
    <Row: Samuel Beckett, Malone Muert, 120, Modernism>
    
    table.rows
    [<Row: Samuel Beckett, Malone Muert, 120, Modernism>,
     <Row: James Joyce, Ulysses, 644, Modernism>,
     <Row: Nicholson Baker, Mezannine, 150, Minimalism>,
     <Row: Vladimir Sorokin, The Queue, 263, Satire>]
    
    # rows, in turn, act like dictionaries
    >>> row = table[1]
    >>> print row['Author']
    James Joyce
    
    # tables can also be faceted
    >>> for t in table.facet_by('Style'):
    ...     print t.faceted_on
    ...     t.table
    Minimalism
    [['Nicholson Baker', 'Mezannine', '150', 'Minimalism']]
    Modernism
    [['Samuel Beckett', 'Malone Muert', '120', 'Modernism'],
     ['James Joyce', 'Ulysses', '644', 'Modernism']]
    Satire
    [['Vladimir Sorokin', 'The Queue', '263', 'Satire']]


To do:

 - formatting
 - options (need to figure out how soon options passed to TableFu.__init__ are executed)
 - output (this should, eventually, output HTML)

More documentation coming.
