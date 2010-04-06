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
    """
    def __init__(self, csv_file, **options):
        reader = csv.reader(csv_file)
        self.table = [row for row in reader]
        self._rows = []
        self.deleted_rows = []
        for row in self.table:
            self.add_row(row)

    def add_row(self, row):
        self._rows.append(Row(self, row))

    def rows(self):
        return self._rows

    def delete_row(self, row_num):
        self.deleted_rows.append(self.rows[row_num])
        del self._rows[row_num]


class Row(object):
    """
    A row in a table
    """
    def __init__(self, table, cells):
        self.table = table
        self.cells = [Datum(table, self, cell) for cell in cells]


class Datum(object):
    """
    A piece of data, with a table, row and column
    """
    def __init__(self, table, row, value):
        self.table = table
        self.row = row
        self.value = value
