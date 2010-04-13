#! /usr/bin/env python
import unittest
from table_fu import TableFu

class TableTest(unittest.TestCase):
        
    def setUp(self):
        self.csv_file = open('tests/test.csv')
        self.table = [['Author', 'Best Book', 'Number of Pages', 'Style'],
            ['Samuel Beckett', 'Malone Muert', '120', 'Modernism'],
            ['James Joyce', 'Ulysses', '644', 'Modernism'],
            ['Nicholson Baker', 'Mezannine', '150', 'Minimalism'],
            ['Vladimir Sorokin', 'The Queue', '263', 'Satire']]

    def tearDown(self):
        self.csv_file.close()


class BigTableTest(TableTest):

    def testTable(self):
        t = TableFu(self.csv_file)
        self.table.pop(0)
        self.assertEqual(t.table, self.table)

    def testTableFromList(self):
        t = TableFu(self.table)
        self.table.pop(0)
        self.assertEqual(t.table, self.table)

    def testTableTwoWays(self):
        t1 = TableFu(self.csv_file)
        t2 = TableFu(self.table)
        self.assertEqual(t1.table, t2.table)


class ColumnTest(TableTest):

    def testgetColumns(self):
        t = TableFu(self.csv_file)
        self.assertEqual(t.columns, self.table[0])

    def testsetColumns(self):
        t = TableFu(self.csv_file)
        columns = ['Style', 'Author']
        t.columns = columns
        self.assertEqual(t.columns, columns)
        

class RowTest(TableTest):
    
    def testCountRows(self):
        t = TableFu(self.csv_file)
        self.table.pop(0)
        self.assertEqual(len(t.rows), len(self.table))

    def testGetRow(self):
        t = TableFu(self.csv_file)
        self.assertEqual(t[1], t.rows[1])

    def testCheckRow(self):
        t = TableFu(self.csv_file)
        self.table.pop(0)
        for i, row in enumerate(self.table):
            self.assertEqual(
                t[i].cells,
                self.table[i]
            )

class DatumTest(TableTest):
    
    def testGetDatum(self):
        t = TableFu(self.csv_file)
        for row in t.rows:
            for c in self.table[0]:
                self.assertEqual(c, row[c].column_name)

    def testDatumValues(self):
        t = TableFu(self.csv_file)
        columns = self.table.pop(0)
        for i, row in enumerate(t.rows):
            for index, column in enumerate(columns):
                self.assertEqual(
                    self.table[i][index],
                    str(row[column])
                )

class ErrorTest(TableTest):
    
    def testBadKey(self):
        t = TableFu(self.csv_file)
        for row in t.rows:
            self.assertRaises(
                KeyError,
                row.__getitem__,
                'not-a-key'
            )
    
    def testBadTotal(self):
        t = TableFu(self.csv_file)
        self.assertRaises(ValueError, t.total, 'Author')


class SortTest(TableTest):
    
    def testSort(self):
        t = TableFu(self.csv_file)
        self.table.pop(0)
        self.table.sort(key=lambda row: row[0])
        t.sort('Author')
        self.assertEqual(
            t[0].cells,
            self.table[0]
        )

class ValuesTest(TableTest):

    def testValues(self):
        t = TableFu(self.csv_file)
        self.table.pop(0)
        authors = [row[0] for row in self.table]
        self.assertEqual(authors, t.values('Author'))
    
    def testTotals(self):
        t = TableFu(self.csv_file)
        self.table.pop(0)
        pages = sum([float(row[2]) for row in self.table])
        self.assertEqual(pages, t.total('Number of Pages'))


if __name__ == '__main__':
    unittest.main()
