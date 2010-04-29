#! /usr/bin/env python
import unittest
from table_fu import TableFu
from table_fu.formatting import Formatter


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

class RowColumnTest(TableTest):
     
    def testLimitColumns(self):
        t = TableFu(self.csv_file)
        t.columns = ['Author', 'Style']
        self.assertEqual(
            str(t[0]),
            'Samuel Beckett, Modernism'
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


class FacetTest(TableTest):

    def testFacet(self):
        t = TableFu(self.csv_file)
        tables = t.facet_by('Style')
        style_row = self.table[4]
        self.assertEqual(
            style_row,
            tables[2][0].cells
        )


class OptionsTest(TableTest):
    
    def testSortOption(self):
        t = TableFu(self.csv_file, sorted_by={"Author": {'reverse': True}})
        self.table.pop(0)
        self.table.sort(key=lambda row: row[0], reverse=True)
        self.assertEqual(t[0].cells, self.table[0])


class DatumFormatTest(TableTest):
    
    def setUp(self):
        self.csv_file = open('tests/sites.csv')
    
    def testCellFormat(self):
        t = TableFu(self.csv_file)
        t.formatting = {'Name': {
            'filter': 'link',
            'args': ['URL']
            }
        }
        
        self.assertEqual(
            str(t[0]['Name']),
            '<a href="http://www.chrisamico.com" title="ChrisAmico.com">ChrisAmico.com</a>'
        )

class HTMLTest(TableTest):
    
    def testDatumTD(self):
        
        t = TableFu(self.csv_file)
        beckett = t[0]['Author']
        self.assertEqual(
            beckett.as_td(),
            '<td class="datum">Samuel Beckett</td>'
        )
    
    def testRowTR(self):
        
        t = TableFu(self.csv_file)
        row = t[0]
        self.assertEqual(
            row.as_tr(),
            '<tr id="row0" class="row even"><td class="datum">Samuel Beckett</td><td class="datum">Malone Muert</td><td class="datum">120</td><td class="datum">Modernism</td></tr>'
        )
        
    

class FormatTest(unittest.TestCase):

    def setUp(self):
        self.format = Formatter()


class RegisterTest(FormatTest):

    def testRegister(self):

        def test(value, *args):
            args = list(args)
            args.insert(0, value)
            return args

        self.format.register(test)
        self.assertEqual(test, self.format._filters['test'])
    
    def testIntComma(self):
        
        self.assertEqual(
            self.format(1200, 'intcomma'),
            '1,200'
        )



if __name__ == '__main__':
    unittest.main()
