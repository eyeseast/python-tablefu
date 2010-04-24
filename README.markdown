This is a Python implementation of ProPublica's [TableFu](http://propublica.github.com/table-fu/).
This API is similar, though following Python conventions.

Usage:
------

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
    
    # sort rows
    >>> table.sort('Author')
    >>> table.rows
    [<Row: James Joyce, Ulysses, 644, Modernism>,
     <Row: Nicholson Baker, Mezannine, 150, Minimalism>,
     <Row: Samuel Beckett, Malone Muert, 120, Modernism>,
     <Row: Vladimir Sorokin, The Queue, 263, Satire>]
    
    # sorting is stored
    table.options['sorted_by']
    {'Author': {'reverse': False}}
    
    # which is handy because...
    
    # tables can also be faceted (and options are copied to new tables)
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


Formatting
----------

Filters are just functions that take a value and some number of positional arguments.
New filters can be registered with the included Formatter class.

    >>> from table_fu.formatting import Formatter
    >>> format = Formatter()
    >>> def capitalize(value, *args):
    ...     return str(value).capitalize()
    >>> format.register(capitalize)
    >>> print format('foo', 'capitalize')
    Foo
    
Cells can be formatted according to rules of the table (which carry over if the table is faceted):

    >>> table = TableFu(open('tests/sites.csv'))
    >>> table.columns
    ['Name', 'URL', 'About']
    >>> table.formatting = {
    ... 'Name': {'filter': 'link', 'args': ['URL']}
    ... }
    >>> print table[0]['Name']
    <a href="http://www.chrisamico.com" title="ChrisAmico.com">ChrisAmico.com</a>
    

To do:

 - output (this should, eventually, output HTML)

More documentation coming.
