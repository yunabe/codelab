import pysh

from pysh import SPACE
from pysh import SINGLE_QUOTED_STRING
from pysh import DOUBLE_QUOTED_STRING
from pysh import SUBSTITUTION
from pysh import REDIRECT
from pysh import PIPE
from pysh import LITERAL


import unittest

class TokenizerTest(unittest.TestCase):
  def test0(self):
    tok = pysh.Tokenizer('cat /tmp/www/foo.txt')
    self.assertEquals([(LITERAL, 'cat'),
                       (SPACE, ' '),
                       (LITERAL, '/tmp/www/foo.txt'),
                       ], list(tok))

  def test1(self):
    tok = pysh.Tokenizer('cat        /tmp/www/foo.txt')
    self.assertEquals([(LITERAL, 'cat'),
                       (SPACE, ' '),
                       (LITERAL, '/tmp/www/foo.txt'),
                       ], list(tok))

  def test2(self):
    tok = pysh.Tokenizer(' cat /tmp/www/foo.txt ')
    self.assertEquals([(LITERAL, 'cat'),
                       (SPACE, ' '),
                       (LITERAL, '/tmp/www/foo.txt'),
                       ], list(tok))

  def test2_2(self):
    tok = pysh.Tokenizer('cat\t/tmp/www/foo.txt')
    self.assertEquals([(LITERAL, 'cat'),
                       (SPACE, ' '),
                       (LITERAL, '/tmp/www/foo.txt'),
                       ], list(tok))

  def testSubstitution(self):
    tok = pysh.Tokenizer('echo $a$b$c')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (SUBSTITUTION, '$a'),
                       (SUBSTITUTION, '$b'),
                       (SUBSTITUTION, '$c'),
                       ], list(tok))

  def testSubstitutionWithoutSpace(self):
    tok = pysh.Tokenizer('echo hoge$a')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (LITERAL, 'hoge'),
                       (SUBSTITUTION, '$a'),
                       ], list(tok))

  def testBraceSubstitution(self):
    tok = pysh.Tokenizer('echo hoge${a}')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (LITERAL, 'hoge'),
                       (SUBSTITUTION, '${a}'),
                       ], list(tok))

  def testBraceSubstitutionWithTrailing(self):
    tok = pysh.Tokenizer('echo hoge${a}10')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (LITERAL, 'hoge'),
                       (SUBSTITUTION, '${a}'),
                       (LITERAL, '10'),
                       ], list(tok))

  def testSubstitutionUnderscore(self):
    tok = pysh.Tokenizer('echo $__init__')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (SUBSTITUTION, '$__init__'),
                       ], list(tok))

  def testRedirect(self):
    tok = pysh.Tokenizer('echo a>/tmp/out')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (LITERAL, 'a'),
                       (REDIRECT, '>'),
                       (LITERAL, '/tmp/out'),
                       ], list(tok))

  def testRedirectAppend(self):
    tok = pysh.Tokenizer('echo a>>/tmp/out')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (LITERAL, 'a'),
                       (REDIRECT, '>>'),
                       (LITERAL, '/tmp/out'),
                       ], list(tok))

  def testRedirectInvalidName(self):
    tok = pysh.Tokenizer('echo $10')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (LITERAL, '$'),
                       (LITERAL, '10'),
                       ], list(tok))

  def testRedirectAppend(self):
    tok = pysh.Tokenizer('echo \'abc\'"def"')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (SINGLE_QUOTED_STRING, '\'abc\''),
                       (DOUBLE_QUOTED_STRING, '"def"'),
                       ], list(tok))

if __name__ == '__main__':
  unittest.main()
