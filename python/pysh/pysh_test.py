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

class PyCmd(object):
  def process(self, args, input):
    for arg in args:
      yield arg
    for line in input:
      yield line.rstrip('\n')

pysh.register_pycmd('pycmd', PyCmd())


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

  def testExpression(self):
    tok = pysh.Tokenizer('echo ${{1: 10}}')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (SUBSTITUTION, '${{1: 10}}'),
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
      if e.errno != 2:
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

  def testBuiltinVar(self):
    map_str = str(map)
    pysh.run('echo $map > out.txt', globals(), locals())
    self.assertEquals(map_str + '\n', file('out.txt').read())

  def testExpression(self):
    map_str = str(map)
    pysh.run('echo ${{len("abc") :[3 * 4 + 10]}} > out.txt', globals(), locals())
    self.assertEquals('{3: [22]}\n', file('out.txt').read())

  def testEnvVar(self):
    os.environ['YUNABE_PYSH_TEST_VAR'] = 'foobarbaz'
    pysh.run('echo $YUNABE_PYSH_TEST_VAR > out.txt', globals(), locals())
    self.assertEquals('foobarbaz\n', file('out.txt').read())

  def testStringArgs(self):
    pysh.run('python -c "import sys;print sys.argv" '
             '"a b" \'c d\' e f > out.txt', globals(), locals())
    argv = eval(file('out.txt').read())
    self.assertEquals(['-c', 'a b', 'c d', 'e', 'f'], argv)

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

  def testPyCmd(self):
    pysh.run('echo "foo\\nbar" | pycmd a b c | cat > out.txt',
             globals(), locals())
    self.assertEquals('pycmd\na\nb\nc\nfoo\nbar\n', file('out.txt').read())

  def testPyCmdSequence(self):
    pysh.run('echo "foo" | pycmd bar | pycmd baz | cat > out.txt',
             globals(), locals())
    self.assertEquals('pycmd\nbaz\npycmd\nbar\nfoo\n', file('out.txt').read())

  def testPyCmdSequence(self):
    pysh.run('echo "foo" | pycmd bar | pycmd baz | cat > out.txt',
             globals(), locals())
    self.assertEquals('pycmd\nbaz\npycmd\nbar\nfoo\n', file('out.txt').read())

  def testReceiveData(self):
    recv = pysh.recv()
    pysh.run('echo "foo bar" | $recv', globals(), locals())
    self.assertTrue(isinstance(recv.input, file))
    self.assertEquals('foo bar\n', recv.input.read())

  def testSendData(self):
    data = ['foo', 'bar', 'baz']
    pysh.run('send $data | sort > out.txt', globals(), locals())
    self.assertEquals('bar\nbaz\nfoo\n', file('out.txt').read())


if __name__ == '__main__':
  unittest.main()
