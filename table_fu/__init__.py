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
    
    TableFu reads in an CSV open file (can also be a URL),
    parsing it into a table property, Row and Datum objects.
    """
    def __init__(self, csv_file, **options):
        reader = csv.reader(csv_file)
        self.table = [row for row in reader]


class Row(object):
    """
    A row in a table
    """
    def __init__(self, table, cells):
        pass

class Datum(object):
    pass
