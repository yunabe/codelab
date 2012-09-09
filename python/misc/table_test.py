from StringIO import StringIO
import math
import unittest

from table import Table, Row

class TableTest(unittest.TestCase):
    def testBasic(self):
        table = Table(['a', 'b'])
        row = table.add_row([1, 2])
        self.assertEquals((1, 2), (row['a'], row['b']))
        self.assertEquals((1, 2), (row.a, row.b))
        self.assertEquals(1, len(list(table)))

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

    def testWhere(self):
        table = Table(['a', 'b'])
        row = table.add_row([1, 5])
        row = table.add_row([7, 4])
        row = table.add_row([5, 6])

        table = table.orderby('a')
        rows = list(table.rows())
        self.assertEquals(3, len(rows))
        self.assertEquals((1, 5), (rows[0].a, rows[0].b))
        self.assertEquals((5, 6), (rows[1].a, rows[1].b))
        self.assertEquals((7, 4), (rows[2].a, rows[2].b))

        table = table.orderby('b')
        rows = list(table.rows())
        self.assertEquals(3, len(rows))
        self.assertEquals((7, 4), (rows[0].a, rows[0].b))
        self.assertEquals((1, 5), (rows[1].a, rows[1].b))
        self.assertEquals((5, 6), (rows[2].a, rows[2].b))

        def f(a):
            return a % 2
        table = table.orderby('math.pow(f(b), 1)', globals(), locals())
        rows = list(table.rows())
        self.assertEquals(3, len(rows))
        self.assertEquals((7, 4), (rows[0].a, rows[0].b))
        self.assertEquals((5, 6), (rows[1].a, rows[1].b))
        self.assertEquals((1, 5), (rows[2].a, rows[2].b))

    def testPrettyPrint(self):
        io = StringIO()
        table = Table(['a', 'b'])
        row = table.add_row([10, 2])
        row = table.add_row([1, 400])
        table.pretty_print(io, sep=' |')
        self.assertEquals(' a |  b\n-------\n10 |  2\n 1 |400\n', io.getvalue())


if __name__ == '__main__':
    unittest.main()
