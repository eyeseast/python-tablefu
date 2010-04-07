#! /usr/bin/env python
"""
This is a Python version of Propublica's TableFu Ruby library.

TableFu parses, sorts and formats table-like streams, like CSVs,
and outputs tables in HTML. It's meant as a utility to make 
getting tabular on the web easier.
"""
import csv
import urllib2


class TableFu(object):
    """
    A table, to be manipulated like a spreadsheet.
    
    TableFu reads in an open CSV file, parsing it 
    into a table property, Row and Datum objects.
    
    Usage:
    
    # test.csv
    
    Author,Best Book,Number of Pages,Style
    Samuel Beckett,Malone Muert,120,Modernism
    James Joyce,Ulysses,644,Modernism
    Nicholson Baker,Mezannine,150,Minimalism
    Vladimir Sorokin,The Queue,263,Satire
    
    >>> spreadsheet = TableFu(open('test.csv'))
    >>> len(spreadsheet.rows)
    4
    >>> spreadsheet.columns
    ['Author', 'Best Book', 'Number of Pages', 'Style']
    >>> spreadsheet.columns = ['Style', 'Author']
    
    
    """
    def __init__(self, csv_file, **options):
        reader = csv.reader(csv_file)
        self.table = [row for row in reader]
        self.column_headers = options.get('columns', None) or self.table[0]
        self.deleted_rows = []
        self.options = options

    def add_rows(self, *rows):
        for row in rows:
            self.table.append(row)

    def rows(self):
        return [Row(row, i, self) for i, row in enumerate(self.table[:1])]

    def delete_row(self, row_num):
        self.deleted_rows.append(self.table[row_num])
        del self.table[row_num]


class Row(object):
    """
    A row in a table
    """
    def __init__(self, cells, row_num, table):
        self.table = table
        self.row_num = row_num
        self.cells = [Datum(table, self, cell) for cell in cells]


class Datum(object):
    """
    A piece of data, with a table, row and column
    """
    def __init__(self, value, row_num, column_name, table):
        self.value = value
        self.row_num = row_num
        self.column_name = column_name
        self.table = table
