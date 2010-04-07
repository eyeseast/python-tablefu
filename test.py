#! /usr/bin/env python
import unittest
from table_fu import TableFu

class TableTest(unittest.TestCase):

    table = [['Author', 'Best Book', 'Number of Pages', 'Style'],
        ['Samuel Beckett', 'Malone Muert', '120', 'Modernism'],
        ['James Joyce', 'Ulysses', '644', 'Modernism'],
        ['Nicholson Baker', 'Mezannine', '150', 'Minimalism'],
        ['Vladimir Sorokin', 'The Queue', '263', 'Satire']]
        
    def setUp(self):
        self.csv_file = open('tests/test.csv')

    def tearDown(self):
        self.csv_file.close()

class ColumnTest(TableTest):

    def testgetColumns(self):
        t = TableFu(self.csv_file)
        self.assertEqual(t.columns, self.table[0])

    def testsetColumns(self):
        t = TableFu(self.csv_file)
        columns = ['Style', 'Author']
        t.columns = columns
        self.assertEquals(t.columns, columns)
        

class RowTest(TableTest):
    
    def testCountRows(self):
        t = TableFu(self.csv_file)
        self.assertEqual(len(t.rows), len(self.table))

    def testGetRow(self):
        t = TableFu(self.csv_file)
        self.assertEqual(t[1], t.rows[1])

    def testCheckRow(self):
        t = TableFu(self.csv_file)
        for i, row in enumerate(self.table[1:]):
            self.assertEqual(
                t[i].cells,
                self.table[i+1] # because we're skipping a row
            )

if __name__ == '__main__':
    unittest.main()
