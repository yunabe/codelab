import csv
import os
import parser
import re
import tokenize
import token
import StringIO
import subprocess
import sys
import threading

SPACE = 'space'
SINGLE_QUOTED_STRING = 'single_quoted'
DOUBLE_QUOTED_STRING = 'double_quoted'
SUBSTITUTION = 'substitution'
REDIRECT = 'redirect'
PIPE = 'pipe'
LITERAL = 'literal'
AND_OP = 'andop'
OR_OP = 'orop'
PARENTHESIS_START = 'parenthesis_start'
PARENTHESIS_END = 'parenthesis_end'
EOF = 'eof'

REDIRECT_PATTERN = re.compile(r'(\d*)>(>)?(?:&(\d+))?')
SPACE_PATTERN = re.compile(r'[ \t]+')
VARIABLE_PATTERN = re.compile(r'\$[_a-zA-Z_][_a-zA-Z0-9]*')
PIPE_PATTERN = re.compile(r'\|')
SINGLE_DOLLAR_PATTERN = re.compile(r'\$')
AND_OPERATOR_PATTERN = re.compile(r'&&')
PARENTHESIS_START_PATTERN = re.compile(r'\(')
PARENTHESIS_END_PATTERN = re.compile(r'\)')
OR_OPERATOR_PATTERN = re.compile(r'\|\|')


class RegexMather(object):
  def __init__(self, regex, type, ignore_space):
    self.__pattern = re.compile(regex)
    self.__type = type
    self.__ignore_space = ignore_space

  def consume(self, input):
    consumed = 0
    if self.__ignore_space:
      match = SPACE_PATTERN.match(input)
      if match:
        consumed += match.end()
        input = input[match.end():]
    match = self.__pattern.match(input) 
    if not match:
      return None, None, 0
    string = match.group(0)
    consumed += len(string)
    input = input[len(string):]
    if self.__ignore_space:
      match = SPACE_PATTERN.match(input)
      if match:
        consumed += match.end()
    return self.__type, string, consumed


class StringMatcher(object):
  def consume(self, input):
    type = None
    if input.startswith('"'):
      type = DOUBLE_QUOTED_STRING
    elif input.startswith('\''):
      type = SINGLE_QUOTED_STRING

    if type is not None:
      toks = tokenize.generate_tokens(StringIO.StringIO(input).readline)
      tok = toks.next()
      if tok[0] == token.STRING:
        return type, tok[1], len(tok[1])
      else:
        raise Exception('Wrong string format')
    else:
      return None, None, 0


class ExprMatcher(object):
  def consume(self, input):
    if not input.startswith('${'):
      return None, None, 0
    input = input[2:]
    try:
      parser.expr(input)
      raise Exception('Expected } but EOF found.')
    except SyntaxError, e:
      if input[e.offset - 1] != '}':
        raise
    expr = input[:e.offset - 1]
    parser.expr(expr)
    string = '${%s}' % expr
    return SUBSTITUTION, string, len(string)


class Tokenizer(object):
  def __init__(self, input):
    self.__input = input.strip()
    self.__eof = False
    self.__matchers = [
      RegexMather(REDIRECT_PATTERN, REDIRECT, True),
      RegexMather(AND_OPERATOR_PATTERN, AND_OP, True),
      # should precede PIPE_PATTERN
      RegexMather(OR_OPERATOR_PATTERN, OR_OP, True),
      RegexMather(PIPE_PATTERN, PIPE, True),
      RegexMather(PARENTHESIS_START_PATTERN, PARENTHESIS_START, True),
      RegexMather(PARENTHESIS_END_PATTERN, PARENTHESIS_END, True),
      StringMatcher(),
      RegexMather(VARIABLE_PATTERN, SUBSTITUTION, False),
      ExprMatcher(),
      RegexMather(SINGLE_DOLLAR_PATTERN, LITERAL, False),
      RegexMather(SPACE_PATTERN, SPACE, False),
      ]

  def __iter__(self):
    return self

  def find_char(self, s, cond):
    for i, c in enumerate(s):
      if cond(c):
        return i
    return -1

  def is_special(self, c):
    if ord(c) <= ord(' '):  # whitespace
      return True
    if c == '$':
      return True
    if c == '>':
      return True
    if c == '|':
      return True
    if c == '&':
      return True
    if c == '(':
      return True
    if c == ')':
      return True

  def next(self):
    self.cur = self.__next()
    return self.cur

  def __next(self):
    input = self.__input
    if not input:
      if self.__eof:
        raise StopIteration()
      else:
        self.__eof = True
        return EOF, ''

    for matcher in self.__matchers:
      token, string, consumed = matcher.consume(input)
      if token is not None:
        self.__input = self.__input[consumed:]
        if token == SPACE:
          return token, ' '
        else:
          return token, string

    pos = self.find_char(input, self.is_special)
    assert pos != 0
    if pos == -1:
      self.__input = ''
      return LITERAL, input
    else:
      self.__input = input[pos:]
      return LITERAL, input[:pos]


class Process(object):
  def __init__(self, args, redirects, is_last):
    self.args = args
    self.redirects = redirects
    self.is_last = is_last


class Parser(object):
  def __init__(self, tokenizer):
    self.__tokenizer = tokenizer

  def parse(self):
    token_stack = []
    for tok in self.__tokenizer:
      if tok[0] == PIPE or tok[0] == EOF:
        if not token_stack:
          raise Exception('Parse error - pipe without command.')
        token_stack.append((EOF, ''))
        proc = self.parseProcess(token_stack, tok[0] == EOF)
        token_stack = []
        yield proc
      else:
        token_stack.append(tok)

  def NotControlToken(self, tok):
    return (tok[0] == LITERAL or
            tok[0] == SINGLE_QUOTED_STRING or
            tok[0] == DOUBLE_QUOTED_STRING or
            tok[0] == SUBSTITUTION)

  def appendToken(self, tok, tokens):
    if tok[0] == DOUBLE_QUOTED_STRING:
      tokens.extend(DoubleQuotedStringExpander(eval(tok[1])))
    else:
      tokens.append(tok)

  def parseRedirectToken(self, tok):
    m = REDIRECT_PATTERN.match(tok[1])
    src_num = sys.stdout.fileno()
    if m.group(1):
      src_num = int(m.group(1))
    append = False
    if m.group(2):
      append = True
    dst_num = -1
    if m.group(3):
      dst_num = int(m.group(3))
    if append and dst_num != -1:
      raise Exception('Can not use both >> and &%d.' % dst_num)
    return append, src_num, dst_num

  def parseProcess(self, tokens, is_last):
    assert tokens
    assert tokens[len(tokens) - 1][0] == EOF
    args = []
    redirects = []
    i = 0
    while True:
      tok = tokens[i]
      if self.NotControlToken(tok):
        arg = []
        args.append(arg)
        while self.NotControlToken(tokens[i]):
          self.appendToken(tokens[i], arg)
          i += 1
      elif tok[0] == REDIRECT:
        append, src_num, dst_num = self.parseRedirectToken(tok)
        if dst_num != -1:
          redirects.append((append, src_num, dst_num))
          i += 1
        else:
          i += 1
          if tokens[i][0] == SPACE:
            # skip space
            i += 1
          if not self.NotControlToken(tokens[i]):
            raise Exception('Parse error - No direction target.')
          target = []
          redirects.append((append, src_num, target))
          while self.NotControlToken(tokens[i]):
            self.appendToken(tokens[i], target)
            i += 1
      elif tok[0] == SPACE:
        i += 1
      elif tok[0] == EOF:
        break
      else:
        raise Exception('Unexpected token: %s' % tok[0])
    return Process(args, redirects, is_last)
      

class DoubleQuotedStringExpander(object):
  def __init__(self, input):
    self.__input = input
    self.__var_matcher = RegexMather(VARIABLE_PATTERN, SUBSTITUTION, False)
    self.__expr_matcher = ExprMatcher()
    
  def __iter__(self):
    return self

  def next(self):
    input = self.__input
    if not input:
      raise StopIteration()
    if input[0] == '$':
      token, string, consumed = self.__var_matcher.consume(input)
      if token is None:
        token, string, consumed = self.__expr_matcher.consume(input)
      if token is None:
        token, string, consumed = LITERAL, '$', 1
      self.__input = input[consumed:]
      return token, string
    else:
      pos = input.find('$')
      if pos == -1:
        self.__input = ''
        return LITERAL, input
      else:
        self.__input = input[pos:]
        return LITERAL, input[:pos]


class VarDict(object):
  def __init__(self, globals, locals):
    self.__globals = globals
    self.__locals = locals

  def __getitem__(self, key):
    if key in self.__locals:
      return self.__locals[key]
    if key in self.__globals:
      return self.__globals[key]
    if key in os.environ:
      return os.environ[key]
    if hasattr(__builtins__, key):
      return getattr(__builtins__, key)
    raise KeyError(key)


__pycmd_map = {}


def register_pycmd(name, pycmd):
  __pycmd_map[name] = pycmd


def get_pycmd(name):
  if isinstance(name, str) and name in __pycmd_map:
    return __pycmd_map[name]
  elif hasattr(name, 'process'):
    return name
  else:
    return None

class PyCmdRunner(threading.Thread):
  def __init__(self, pycmd_stack, r, w):
    threading.Thread.__init__(self)
    assert pycmd_stack
    self.__pycmd_stack = pycmd_stack
    self.__r = r
    self.__w = w

  def run(self):
    # Creates w first to close self.__w for sure.
    if self.__w != -1:
      w = os.fdopen(self.__w, 'w')
    else:
      w = sys.stdout
    if self.__r == -1:
      out = None
    else:
      out = os.fdopen(self.__r, 'r')
    for i, (pycmd, args, redirects) in enumerate(self.__pycmd_stack):
      if redirects:
        if w is not sys.stdout or i != len(self.__pycmd_stack) - 1:
          raise Exception('redirect with pycmd is allowed '
                          'only when it is the last.')
        if len(redirects) != 1:
          raise Exception('multi-redirect with pycmd is not allowed.')

        redirect = redirects[0]
        if isinstance(redirect[2], int):
          raise Exception('Redirect to another file descriptor is not allowed.')
        if redirect[0]:
          mode = 'a'  # >>
        else:
          mode = 'w'  # >
        w = file(redirect[2], mode)

      out = pycmd.process(args, out)

    for data in out:
      w.write(str(data) + '\n')
      w.flush()  # can be inefficient.


class Evaluator(object):
  def __init__(self, parser):
    self.__parser = parser

  def evalSubstitution(self, value, globals, locals):
    if value.startswith('${'):
      # remove ${ and }
      name = value[2:-1]
    else:
      # remove $
      name = value[1:]
    return eval(name, None, VarDict(globals, locals))

  def evalArg(self, arg, globals, locals):
    assert arg
    w = StringIO.StringIO()
    values = []
    for tok in arg:
      if tok[0] == LITERAL:
        values.append(tok[1])
      elif tok[0] == SINGLE_QUOTED_STRING:
        values.append(eval(tok[1]))
      elif tok[0] == SUBSTITUTION:
        values.append(self.evalSubstitution(tok[1], globals, locals))
      else:
        raise Exception('Unexpected token: %s' % tok[0])
    if len(values) > 1:
      return ''.join(map(str, values))
    else:
      return values[0]

  def execute(self, globals, locals):
    pids = {}
    old_r = -1
    pycmd_stack = []
    runners = []
    # We need to store list of write-fd for runners to close them
    # in child process!!
    runner_wfd = []  
    for proc in self.__parser.parse():
      is_last = proc.is_last
      args = []
      for arg in proc.args:
        args.append(self.evalArg(arg, globals, locals))
      redirects = []
      for redirect in proc.redirects:
        if isinstance(redirect[2], int):
          redirects.append(redirect)
        else:
          redirects.append((redirect[0], redirect[1],
                            str(self.evalArg(redirect[2], globals, locals))))

      pycmd = get_pycmd(args[0])
      if pycmd:
        pycmd_stack.append((pycmd, args, redirects))
        continue

      if pycmd_stack:
        new_r, w = os.pipe()
        runner = PyCmdRunner(pycmd_stack, old_r, w)
        runners.append(runner)
        runner_wfd.append(w)
        old_r = new_r
        pycmd_stack = []

      if not is_last:
        new_r, w = os.pipe()
      pid = os.fork()
      if pid != 0:
        if not is_last:
          # Don't forget to close pipe in the root process.
          os.close(w)
        if old_r != -1:
          os.close(old_r)
        pids[pid] = w if not is_last else None
        if not is_last:
          old_r = new_r
      else:
        for fd in runner_wfd:
          os.close(fd)
        if not is_last:
          os.dup2(w, sys.stdout.fileno())
        if old_r != -1:
          os.dup2(old_r, sys.stdin.fileno())
        for redirect in redirects:
          if isinstance(redirect[2], int):
            os.dup2(redirect[2], redirect[1])
          else:
            if redirect[0]:
              mode = 'a'  # >>
            else:
              mode = 'w'  # >
            f = file(redirect[2], mode)
            os.dup2(f.fileno(), redirect[1])
        # TODO(yunabe): quit a child process if execvp fails.
        str_args = map(str, args)
        os.execvp(str_args[0], str_args)

    if pycmd_stack:
      # pycmd is the last command.
      runner = PyCmdRunner(pycmd_stack, old_r, -1)
      runners.append(runner)

    for runner in runners:
      runner.start()
    for runner in runners:      
      runner.join()

    while len(pids) > 0:
      pid, rc = os.wait()
      w = pids.pop(pid)


class pycmd_send(object):
  def process(self, args, input):
    assert len(args) == 2
    return args[1]


class pycmd_recv(object):
  def process(self, args, input):
    assert len(args) == 2
    l = args[1]
    assert isinstance(l, list)
    l.extend(input)
    return []


class pycmd_map(object):
  def process(self, args, input):
    assert len(args) == 2
    f = args[1]
    assert callable(f)
    return (f(x) for x in input)


class pycmd_filter(object):
  def process(self, args, input):
    assert len(args) == 2
    cond = args[1]
    assert callable(cond)
    for x in input:
      if cond(x):
        yield x


class pycmd_reduce(object):
  def process(self, args, input):
    assert len(args) == 2
    f = args[1]
    assert callable(f)
    return [reduce(f, input)]


class pycmd_readcsv(object):
  def process(self, args, input):
    return csv.reader(input)


register_pycmd('send', pycmd_send())
register_pycmd('recv', pycmd_recv())
register_pycmd('map', pycmd_map())
register_pycmd('filter', pycmd_filter())
register_pycmd('reduce', pycmd_reduce())
register_pycmd('readcsv', pycmd_readcsv())


def run(cmd_str, globals, locals):
  tok = Tokenizer(cmd_str)
  parser = Parser(tok)
  evaluator = Evaluator(parser)
  evaluator.execute(globals, locals)
