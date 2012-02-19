import pysh

import unittest

class TokenizerTest(unittest.TestCase):
  def test0(self):
    tok = pysh.Tokenizer('cat /tmp/www/foo.txt')
    self.assertEquals(['cat', ' ', '/tmp/www/foo.txt'], list(tok))

  def test1(self):
    tok = pysh.Tokenizer('cat        /tmp/www/foo.txt')
    self.assertEquals(['cat', ' ', '/tmp/www/foo.txt'], list(tok))

  def test2(self):
    tok = pysh.Tokenizer(' cat /tmp/www/foo.txt ')
    self.assertEquals(['cat', ' ', '/tmp/www/foo.txt'], list(tok))

  def test3(self):
    tok = pysh.Tokenizer('cat\t/tmp/www/foo.txt')
    self.assertEquals(['cat', ' ', '/tmp/www/foo.txt'], list(tok))

  def test3(self):
    tok = pysh.Tokenizer('echo $a$b$c')
    self.assertEquals(['echo', ' ', '$a', '$b', '$c'], list(tok))

  def test4(self):
    tok = pysh.Tokenizer('echo hoge$a')
    self.assertEquals(['echo', ' ', 'hoge', '$a'], list(tok))

  def test5(self):
    tok = pysh.Tokenizer('echo hoge${a}')
    self.assertEquals(['echo', ' ', 'hoge', '${a}'], list(tok))

  def test6(self):
    tok = pysh.Tokenizer('echo hoge${a}10')
    self.assertEquals(['echo', ' ', 'hoge', '${a}', '10'], list(tok))

  def test7(self):
    tok = pysh.Tokenizer('echo $__init__')
    self.assertEquals(['echo', ' ', '$__init__'], list(tok))

  def test8(self):
    tok = pysh.Tokenizer('echo a>/tmp/out')
    self.assertEquals(['echo', ' ', 'a', '>', '/tmp/out'], list(tok))

  def test9(self):
    tok = pysh.Tokenizer('echo a>>/tmp/out')
    self.assertEquals(['echo', ' ', 'a', '>>', '/tmp/out'], list(tok))

if __name__ == '__main__':
  unittest.main()
