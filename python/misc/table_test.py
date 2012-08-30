from StringIO import StringIO
import unittest

from table import Table, Row

class TableTest(unittest.TestCase):
    def testBasic(self):
        table = Table(['a', 'b'])
        row = table.add_row([1, 2])
        self.assertEquals((1, 2), (row['a'], row['b']))
        self.assertEquals((1, 2), (row.a, row.b))

    def testWhere(self):
        table = Table(['a', 'b'])
        row = table.add_row([1, 2])
        row = table.add_row([3, 4])
        row = table.add_row([5, 6])

        table = table.where('a != 3')
        rows = list(table.rows())
        self.assertEquals(2, len(rows))
        self.assertEquals((1, 2), (rows[0].a, rows[0].b))
        self.assertEquals((5, 6), (rows[1].a, rows[1].b))

    def testPrettyPrint(self):
        io = StringIO()
        table = Table(['a', 'b'])
        row = table.add_row([10, 2])
        row = table.add_row([1, 400])
        table.pretty_print(io, sep=' |')
        self.assertEquals(' a |  b\n-------\n10 |  2\n 1 |400\n', io.getvalue())


if __name__ == '__main__':
    unittest.main()
