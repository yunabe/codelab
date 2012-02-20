import pysh
from pysh import SPACE
from pysh import SINGLE_QUOTED_STRING
from pysh import DOUBLE_QUOTED_STRING
from pysh import SUBSTITUTION
from pysh import REDIRECT
from pysh import PIPE
from pysh import LITERAL
from pysh import EOF

import os
import shutil
import tempfile
import unittest

class TokenizerTest(unittest.TestCase):
  def test0(self):
    tok = pysh.Tokenizer('cat /tmp/www/foo.txt')
    self.assertEquals([(LITERAL, 'cat'),
                       (SPACE, ' '),
                       (LITERAL, '/tmp/www/foo.txt'),
                       (EOF, ''),
                       ], list(tok))

  def test1(self):
    tok = pysh.Tokenizer('cat        /tmp/www/foo.txt')
    self.assertEquals([(LITERAL, 'cat'),
                       (SPACE, ' '),
                       (LITERAL, '/tmp/www/foo.txt'),
                       (EOF, ''),
                       ], list(tok))

  def test2(self):
    tok = pysh.Tokenizer(' cat /tmp/www/foo.txt ')
    self.assertEquals([(LITERAL, 'cat'),
                       (SPACE, ' '),
                       (LITERAL, '/tmp/www/foo.txt'),
                       (EOF, ''),
                       ], list(tok))

  def test2_2(self):
    tok = pysh.Tokenizer('cat\t/tmp/www/foo.txt')
    self.assertEquals([(LITERAL, 'cat'),
                       (SPACE, ' '),
                       (LITERAL, '/tmp/www/foo.txt'),
                       (EOF, ''),
                       ], list(tok))

  def testSubstitution(self):
    tok = pysh.Tokenizer('echo $a$b$c')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (SUBSTITUTION, '$a'),
                       (SUBSTITUTION, '$b'),
                       (SUBSTITUTION, '$c'),
                       (EOF, ''),
                       ], list(tok))

  def testSubstitutionWithoutSpace(self):
    tok = pysh.Tokenizer('echo hoge$a')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (LITERAL, 'hoge'),
                       (SUBSTITUTION, '$a'),
                       (EOF, ''),
                       ], list(tok))

  def testBraceSubstitution(self):
    tok = pysh.Tokenizer('echo hoge${a}')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (LITERAL, 'hoge'),
                       (SUBSTITUTION, '${a}'),
                       (EOF, ''),
                       ], list(tok))

  def testBraceSubstitutionWithTrailing(self):
    tok = pysh.Tokenizer('echo hoge${a}10')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (LITERAL, 'hoge'),
                       (SUBSTITUTION, '${a}'),
                       (LITERAL, '10'),
                       (EOF, ''),
                       ], list(tok))

  def testSubstitutionUnderscore(self):
    tok = pysh.Tokenizer('echo $__init__')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (SUBSTITUTION, '$__init__'),
                       (EOF, ''),
                       ], list(tok))

  def testRedirect(self):
    tok = pysh.Tokenizer('echo a>/tmp/out')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (LITERAL, 'a'),
                       (REDIRECT, '>'),
                       (LITERAL, '/tmp/out'),
                       (EOF, ''),
                       ], list(tok))

  def testRedirectAppend(self):
    tok = pysh.Tokenizer('echo a>>/tmp/out')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (LITERAL, 'a'),
                       (REDIRECT, '>>'),
                       (LITERAL, '/tmp/out'),
                       (EOF, ''),
                       ], list(tok))

  def testRedirectInvalidName(self):
    tok = pysh.Tokenizer('echo $10')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (LITERAL, '$'),
                       (LITERAL, '10'),
                       (EOF, ''),
                       ], list(tok))

  def testRedirectAppend(self):
    tok = pysh.Tokenizer('echo \'abc\'"def"')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (SINGLE_QUOTED_STRING, '\'abc\''),
                       (DOUBLE_QUOTED_STRING, '"def"'),
                       (EOF, ''),
                       ], list(tok))


class DoubleQuotedStringExpanderTest(unittest.TestCase):
  def test(self):
    tok = pysh.Tokenizer('echo "apple pie. a$bc e${fg}\t10"')
    expanded = pysh.DoubleQuotedStringExpander('apple pie. a$bc e${fg}\t10')
    self.assertEquals([(LITERAL, 'apple pie. a'),
                       (SUBSTITUTION, '$bc'),
                       (LITERAL, ' e'),
                       (SUBSTITUTION, '${fg}'),
                       (LITERAL, '\t10'),
                       ], list(expanded))


class TempDir(object):
  def __init__(self):
    self.path = None

  def __enter__(self):
    self.path = tempfile.mkdtemp()
    return self

  def __exit__(self, type, value, traceback):
    if not self.path:
      return
    try:
      shutil.rmtree(self.path)
    except OSError, e:
      if e.errorno != 2:
        raise
    self.path = None


class RunTest(unittest.TestCase):
  def setUp(self):
    self.original_dir = os.getcwd()
    self.tmpdir = TempDir()
    self.tmpdir.__enter__()
    os.chdir(self.tmpdir.path)

  def tearDown(self):
    self.tmpdir.__exit__(None, None, None)
    os.chdir(self.original_dir)

  def testRedirect(self):
    pysh.run('echo foo bar > out.txt', globals(), locals())
    self.assertEquals('foo bar\n', file('out.txt').read())

  def testAppendRedirect(self):
    pysh.run('echo foo > out.txt', globals(), locals())
    pysh.run('echo bar >> out.txt', globals(), locals())
    self.assertEquals('foo\nbar\n', file('out.txt').read())

  def testPipe(self):
    file('tmp.txt', 'w').write('a\nb\nc\n')
    pysh.run('cat tmp.txt | grep -v b > out.txt', globals(), locals())
    self.assertEquals('a\nc\n', file('out.txt').read())

  def testVar(self):
    message = 'Hello world.'
    pysh.run('echo $message > out.txt', globals(), locals())
    self.assertEquals('Hello world.\n', file('out.txt').read())

  def testGlobalVar(self):
    pysh.run('echo $__name__ > out.txt', globals(), locals())
    self.assertEquals('__main__\n', file('out.txt').read())

  def testNumberedRedirect(self):
    pysh.run('python -c "import sys;'
             'print >> sys.stderr, \'error\';print \'out\'"'
             '> stdout.txt 2> stderr.txt',
             globals(), locals())
    self.assertEquals('error\n', file('stderr.txt').read())
    self.assertEquals('out\n', file('stdout.txt').read())

  def testDivertRedirect(self):
    pysh.run('python -c "import sys;'
             'print >> sys.stderr, \'error\';print \'out\'"'
             '>out.txt 2>&1', globals(), locals())
    self.assertEquals('error\nout\n', file('out.txt').read())


if __name__ == '__main__':
  unittest.main()
