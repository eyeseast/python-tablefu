#! /usr/bin/env python
import csv
import unittest
import urllib2
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
        "Create a table from an open CSV file"
        t = TableFu(self.csv_file)
        self.table.pop(0)
        self.assertEqual(t.table, self.table, 4)

    def testTableFromList(self):
        "Create a table from a two-dimensional list"
        t = TableFu(self.table)
        self.table.pop(0)
        self.assertEqual(t.table, self.table)

    def testTableTwoWays(self):
        "Two ways to create the same table"
        t1 = TableFu(self.csv_file)
        t2 = TableFu(self.table)
        self.assertEqual(t1.table, t2.table)


class ColumnTest(TableTest):

    def testgetColumns(self):
        "Get a table's (default) columns"
        t = TableFu(self.csv_file)
        self.assertEqual(t.columns, self.table[0])

    def testsetColumns(self):
        "Set new columns for a table"
        t = TableFu(self.csv_file)
        columns = ['Style', 'Author']
        t.columns = columns
        self.assertEqual(t.columns, columns)
        

class RowTest(TableTest):
    
    def testCountRows(self):
        "Count rows, not including headings"
        t = TableFu(self.csv_file)
        self.table.pop(0)
        self.assertEqual(len(t.rows), len(self.table), 4)

    def testGetRow(self):
        "Get one row by slicing the table"
        t = TableFu(self.csv_file)
        self.assertEqual(t[1], t.rows[1])

    def testCheckRow(self):
        "Check that row numbers are assigned correctly"
        t = TableFu(self.csv_file)
        self.table.pop(0)
        for i, row in enumerate(self.table):
            self.assertEqual(
                t[i].cells,
                self.table[i]
            )

class RowColumnTest(TableTest):
     
    def testLimitColumns(self):
        "Column definitions are passed to rows"
        t = TableFu(self.csv_file)
        t.columns = ['Author', 'Style']
        self.assertEqual(
            str(t[0]),
            'Samuel Beckett, Modernism'
            )


class DatumTest(TableTest):
    
    def testGetDatum(self):
        "Get one cell at a time"
        t = TableFu(self.csv_file)
        for row in t.rows:
            for c in self.table[0]:
                self.assertEqual(c, row[c].column_name)

    def testSetDatum(self):
        "Set a new value for one cell"
        t = TableFu(self.csv_file)
        modernism = t[0]
        modernism['Author'] = "Someone new"
        self.assertEqual(str(modernism['Author']), "Someone new")

    def testDatumValues(self):
        "Ensure every cell has the right value"
        t = TableFu(self.csv_file)
        columns = self.table.pop(0)
        for i, row in enumerate(t.rows):
            for index, column in enumerate(columns):
                self.assertEqual(
                    self.table[i][index],
                    str(row[column])
                )
    
    def testUpdateValues(self):
        "Update multiple cell values for a given row"
        t = TableFu(self.csv_file)
        modernism = t[0]
        kerouac = {
            'Author': 'Jack Kerouac',
            'Best Book': 'On the Road',
            'Number of Pages': '320',
            'Style': 'Beat'
        }
        modernism.update(kerouac)
        self.assertEqual(
            set(kerouac.values()),
            set(modernism.cells)
        )
    
    def testKeys(self):
        "Get keys for a row, which should match the table's columns"
        t = TableFu(self.csv_file)
        modernism = t[0]
        self.assertEqual(modernism.keys(), t.columns)
    
    def testValues(self):
        "Get values for a row"
        t = TableFu(self.csv_file)
        modernism = t[0]
        values = [d.value for d in modernism.data]
        self.assertEqual(modernism.values(), values)
    
    def testItems(self):
        "Get key-value pairs for a row"
        t = TableFu(self.csv_file)
        modernism = t[0]
        self.assertEqual(
            modernism.items(),
            zip(modernism.keys(), modernism.values())
        )
    
    def testListRow(self):
        "Convert a row back to a list"
        t = TableFu(self.csv_file)
        modernism = t[0]
        self.assertEqual(
            list(modernism),
            modernism.values()
        )
        
class ErrorTest(TableTest):
    
    def testBadKey(self):
        "Non-existent columns raise a KeyError"
        t = TableFu(self.csv_file)
        for row in t.rows:
            self.assertRaises(
                KeyError,
                row.__getitem__,
                'not-a-key'
            )
    
    def testBadTotal(self):
        "Only number-like fields can be totaled"
        t = TableFu(self.csv_file)
        self.assertRaises(ValueError, t.total, 'Author')


class SortTest(TableTest):
    
    def testSort(self):
        "Sort a table in place"
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
        "Return one column's values for all rows"
        t = TableFu(self.csv_file)
        self.table.pop(0)
        authors = [row[0] for row in self.table]
        self.assertEqual(authors, t.values('Author'))
    
    def testTotals(self):
        "Total values for a table across rows"
        t = TableFu(self.csv_file)
        self.table.pop(0)
        pages = sum([float(row[2]) for row in self.table])
        self.assertEqual(pages, t.total('Number of Pages'))


class FacetTest(TableTest):

    def testFacet(self):
        "Facet tables based on shared column values"
        t = TableFu(self.csv_file)
        tables = t.facet_by('Style')
        style_row = self.table[4]
        self.assertEqual(
            style_row,
            tables[2][0].cells
        )


class OptionsTest(TableTest):
    
    def testSortOption(self):
        "Pass in options as keyword arguments"
        t = TableFu(self.csv_file, sorted_by={"Author": {'reverse': True}})
        self.table.pop(0)
        self.table.sort(key=lambda row: row[0], reverse=True)
        self.assertEqual(t[0].cells, self.table[0])


class DatumFormatTest(TableTest):
    
    def setUp(self):
        self.csv_file = open('tests/sites.csv')
    
    def testCellFormat(self):
        "Format a cell"
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
        "Output a cell as a <td> element"
        t = TableFu(self.csv_file)
        beckett = t[0]['Author']
        self.assertEqual(
            beckett.as_td(),
            '<td class="datum">Samuel Beckett</td>'
        )
    
    def testRowTR(self):
        "Output a row as a <tr> element"
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
        "Register a new format function"

        def test(value, *args):
            args = list(args)
            args.insert(0, value)
            return args

        self.format.register(test)
        self.assertEqual(test, self.format._filters['test'])
    
    def testIntComma(self):
        "Use intcomma for nicer number formatting"
        self.assertEqual(
            self.format(1200, 'intcomma'),
            '1,200'
        )

class RemoteTest(unittest.TestCase):
    
    def testUseURL(self):
        "Use a response from urllib2.urlopen as our base file"
        url = "http://spreadsheets.google.com/pub?key=thJa_BvqQuNdaFfFJMMII0Q&output=csv"
        response1 = urllib2.urlopen(url)
        response2 = urllib2.urlopen(url)
        reader = csv.reader(response1)
        columns = reader.next()
        t = TableFu(response2)
        self.assertEqual(columns, t.columns)


if __name__ == '__main__':
    unittest.main()
