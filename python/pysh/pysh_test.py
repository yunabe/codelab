import pysh
from pysh import SPACE
from pysh import SINGLE_QUOTED_STRING
from pysh import DOUBLE_QUOTED_STRING
from pysh import SUBSTITUTION
from pysh import REDIRECT
from pysh import PIPE
from pysh import LITERAL
from pysh import AND_OP
from pysh import OR_OP
from pysh import PARENTHESIS_START
from pysh import PARENTHESIS_END
from pysh import EOF

import os
import re
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


class RegexMatherTest(unittest.TestCase):
  def test(self):
    pattern = re.compile(r'abc')
    matcher = pysh.RegexMather(pattern, LITERAL, False)

    type, string, consumed = matcher.consume('abcdefg')
    self.assertEquals(type, LITERAL)
    self.assertEquals(string, 'abc')
    self.assertEquals(consumed, 3)

    type, string, consumed = matcher.consume('abc defg')
    self.assertEquals(type, LITERAL)
    self.assertEquals(string, 'abc')
    self.assertEquals(consumed, 3)

    type, _, _ = matcher.consume(' abcdefg')
    self.assertTrue(type is None)

  def testIgnoreSpace(self):
    pattern = re.compile(r'abc')
    matcher = pysh.RegexMather(pattern, LITERAL, True)

    type, string, consumed = matcher.consume('abcdefg')
    self.assertEquals(type, LITERAL)
    self.assertEquals(string, 'abc')
    self.assertEquals(consumed, 3)

    type, string, consumed = matcher.consume('abc  defg')
    self.assertEquals(type, LITERAL)
    self.assertEquals(string, 'abc')
    self.assertEquals(consumed, 5)

    type, string, consumed = matcher.consume('  abcdefg')
    self.assertEquals(type, LITERAL)
    self.assertEquals(string, 'abc')
    self.assertEquals(consumed, 5)


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
    tok = pysh.Tokenizer('echo $a$b/$c')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (SUBSTITUTION, '$a'),
                       (SUBSTITUTION, '$b'),
                       (LITERAL, '/'),
                       (SUBSTITUTION, '$c'),
                       (EOF, ''),
                       ], list(tok))

  def testSubstitutionWithSpace(self):
    tok = pysh.Tokenizer('echo $a $b /$c')
    self.assertEquals([(LITERAL, 'echo'),
                       (SPACE, ' '),
                       (SUBSTITUTION, '$a'),
                       (SPACE, ' '),
                       (SUBSTITUTION, '$b'),
                       (SPACE, ' '),
                       (LITERAL, '/'),
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

  def testPipe(self):
    tok = pysh.Tokenizer('cat | /tmp/out')
    self.assertEquals([(LITERAL, 'cat'),
                       (PIPE, '|'),
                       (LITERAL, '/tmp/out'),
                       (EOF, ''),
                       ], list(tok))

  def testPipeWithoutSpace(self):
    tok = pysh.Tokenizer('cat|/tmp/out')
    self.assertEquals([(LITERAL, 'cat'),
                       (PIPE, '|'),
                       (LITERAL, '/tmp/out'),
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

  def testAndOrOperator(self):
    tok = pysh.Tokenizer('foo && bar || a&&b||c')
    self.assertEquals([(LITERAL, 'foo'),
                       (AND_OP, '&&'),
                       (LITERAL, 'bar'),
                       (OR_OP, '||'),
                       (LITERAL, 'a'),
                       (AND_OP, '&&'),
                       (LITERAL, 'b'),
                       (OR_OP, '||'),
                       (LITERAL, 'c'),
                       (EOF, ''),
                       ], list(tok))

  def testParenthesis(self):
    tok = pysh.Tokenizer('() a(b)')
    self.assertEquals([(PARENTHESIS_START, '('),
                       (PARENTHESIS_END, ')'),
                       (LITERAL, 'a'),
                       (PARENTHESIS_START, '('),
                       (LITERAL, 'b'),
                       (PARENTHESIS_END, ')'),
                       ('eof', '')], list(tok))


class DoubleQuotedStringExpanderTest(unittest.TestCase):
  def test(self):
    expanded = pysh.DoubleQuotedStringExpander(
      'apple pie. a$bc e${fg}\t10 ${{1: "3}"}}')
    self.assertEquals([(LITERAL, 'apple pie. a'),
                       (SUBSTITUTION, '$bc'),
                       (LITERAL, ' e'),
                       (SUBSTITUTION, '${fg}'),
                       (LITERAL, '\t10 '),
                       (SUBSTITUTION, '${{1: "3}"}}'),
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

  def testPyCmdRedirect(self):
    pysh.run('echo "foo" | pycmd a b c > out.txt',
             globals(), locals())
    self.assertEquals('pycmd\na\nb\nc\nfoo\n', file('out.txt').read())

  def testPyCmdSequence(self):
    pysh.run('echo "foo" | pycmd bar | pycmd baz | cat > out.txt',
             globals(), locals())
    self.assertEquals('pycmd\nbaz\npycmd\nbar\nfoo\n', file('out.txt').read())

  def testPyCmdInVar(self):
    class Tmp(object):
      def process(self, args, input):
        return ['tmp', 19]
    tmp = Tmp()
    pysh.run('$tmp > out.txt', globals(), locals())
    self.assertEquals('tmp\n19\n', file('out.txt').read())

  def testReceiveData(self):
    out = []
    pysh.run('echo "foo\\nbar" | recv $out', globals(), locals())
    self.assertEquals(['foo\n', 'bar\n'], out)

  def testSendData(self):
    data = ['foo', 'bar', 'baz']
    pysh.run('send $data | sort > out.txt', globals(), locals())
    self.assertEquals('bar\nbaz\nfoo\n', file('out.txt').read())

  def testMapCmd(self):
    pysh.run('echo "1\\n2\\n3\\n4\\n5" | map ${lambda l: int(l)} |'
             'map ${lambda x: x * x} > out.txt', globals(), locals())
    self.assertEquals('1\n4\n9\n16\n25\n', file('out.txt').read())

  def testFilterCmd(self):
    pysh.run('echo "cupcake\\ndonut\\nfroyo\\nginger" |'
             'filter ${lambda l: "e" in l} > out.txt',
             globals(), locals())
    self.assertEquals('cupcake\n\nginger\n\n', file('out.txt').read())

  def testReduceCmd(self):
    pysh.run('echo "foo\\nbar" | reduce ${lambda x, y: x.strip() + y.strip()} |'
             'cat > out.txt', globals(), locals())
    self.assertEquals('foobar\n', file('out.txt').read())

  def testReadCvsCmd(self):
    pysh.run('echo \'a,b,"c,"\' > in.txt', globals(), locals())
    pysh.run('echo \'e,"f","""g"""\' >> in.txt', globals(), locals())
    pysh.run('cat in.txt | readcsv |'
             'map ${lambda row: row[2]} > out.txt',
             globals(), locals())
    self.assertEquals('c,\n"g"\n', file('out.txt').read())


if __name__ == '__main__':
  unittest.main()
