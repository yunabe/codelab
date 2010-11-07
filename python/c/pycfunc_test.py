import pycfunc
import unittest

class TestSequenceFunctions(unittest.TestCase):
  def testConcat(self):
    self.assertEqual('Hello world!',
                     pycfunc.concat('Hello ', 'world!'))
  def testSum(self):
    self.assertEqual(13, pycfunc.sum(5, 8))

  def testKeywordArguments(self):
    self.assertEqual(3, pycfunc.divide(6, 2))
    self.assertEqual(4, pycfunc.divide(numerator=8, denominator=2))
    self.assertEqual(5, pycfunc.divide(denominator=3, numerator=15))

  def testList2tuple(self):
    self.assertEqual((1,2,3), pycfunc.list2tuple([1, 2, 3]))

  def testReduce(self):
    self.assertEqual(45, pycfunc.reduce(lambda x, y: x + y, xrange(10)))

if __name__ == '__main__':
  unittest.main()
