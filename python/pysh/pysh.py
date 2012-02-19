import __builtin__
import os
import tokenize
import token
import StringIO
import subprocess
import sys

SPACE = 'space'
SINGLE_QUOTED_STRING = 'single_quoted'
DOUBLE_QUOTED_STRING = 'double_quoted'
SUBSTITUTION = 'substitution'
REDIRECT = 'redirect'
PIPE = 'pipe'
LITERAL = 'literal'
EOF = 'eof'

class LexerBase(object):
  def is_whitespace(self, c):
    return ord(c) <= ord(' ')

  def is_not_whitespace(self, c):
    return not self.is_whitespace(c)

  def is_special(self, c):
    if self.is_whitespace(c):
      return True
    if c == '$':
      return True
    if c == '>':
      return True

  def is_alphabet(self, c):
    if c == '_':
      return True
    ordc = ord(c)
    if ord('a') <= ordc and ordc <= ord('z'):
      return True
    if ord('A') <= ordc and ordc <= ord('Z'):
      return True
    return False

  def is_digit(self, c):
    ordc = ord(c)
    return ord('0') <= ordc and ordc <= ord('9')

  def extract_var(self, input):
    assert input and input[0] == '$'
    if len(input) == 1:
      return '$'
    if input[1] == '{':
      brace = True
      pos = 2
    else:
      brace = False
      pos = 1
    first_char = True
    while pos < len(input) and (
      (first_char and self.is_alphabet(input[pos])) or
      (not first_char and (self.is_alphabet(input[pos]) or
                           self.is_digit(input[pos])))):
      first_char = False
      pos += 1
    if not brace:
      return input[:pos]
    else:
      if not pos < len(input) or input[pos] != '}':
        raise Exception('bad substitution')
      return input[:pos + 1]

  def extract_string(self, input):
    toks = tokenize.generate_tokens(StringIO.StringIO(input).readline)
    tok = toks.next()
    if tok[0] == token.STRING:
      return tok[1]
    else:
      raise Exception('Wrong string format')


class Tokenizer(LexerBase):
  def __init__(self, input):
    self.__input = input.strip()
    self.__eof = False

  def __iter__(self):
    return self

  def find_char(self, s, cond):
    for i, c in enumerate(s):
      if cond(c):
        return i
    return -1

  def next(self):
    input = self.__input
    if not input:
      if self.__eof:
        raise StopIteration()
      else:
        self.__eof = True
        return EOF, ''

    c = input[0]
    if self.is_whitespace(c):
      pos = self.find_char(input, self.is_not_whitespace)
      assert pos != -1
      self.__input = input[pos:]
      return (SPACE, ' ')
    elif c == '|':
      self.__input = input[1:]
      return (PIPE, '|')
    elif c == '"' or c == '\'':
      is_double = c == '"'
      string = self.extract_string(input)
      self.__input = input[len(string):]
      return (DOUBLE_QUOTED_STRING if is_double else SINGLE_QUOTED_STRING,
              string)
    elif c == '$':
      string = self.extract_var(input)
      self.__input = input[len(string):]
      if string == '$':
        return LITERAL, string
      else:
        return SUBSTITUTION, string
    elif c == '>':
      if input.startswith('>>'):
        self.__input = input[2:]
        return (REDIRECT, '>>')
      else:
        self.__input = input[1:]
        return (REDIRECT, '>')
    else:
      pos = self.find_char(input, self.is_special)
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
        i += 1
        if tokens[i][0] == SPACE:
          # skip space
          i += 1
        if not self.NotControlToken(tokens[i]):
          raise Exception('Parse error - No direction target.')
        target = []
        redirects.append((tok[1], target))
        while self.NotControlToken(tokens[i]):
          self.appendToken(tokens[i], target)
          i += 1
      elif tok[0] == SPACE:
        i += 1
      elif tok[0] == EOF:
        break
      else:
        raise Exception('Unexpected error.')
    return Process(args, redirects, is_last)
      

class DoubleQuotedStringExpander(LexerBase):
  def __init__(self, input):
    self.__input = input

  def __iter__(self):
    return self

  def next(self):
    input = self.__input
    if not input:
      raise StopIteration()
    if input[0] == '$':
      string = self.extract_var(input)
      self.__input = input[len(string):]
      if string == '$':
        return LITERAL, string
      else:
        return SUBSTITUTION, string
    else:
      pos = input.find('$')
      if pos == -1:
        self.__input = ''
        return LITERAL, input
      else:
        self.__input = input[pos:]
        return LITERAL, input[:pos]


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
    if name in locals:
      return locals[name]
    elif name in globals:
      return globals[name]
    elif hasattr(__builtin__, name):
      return getattr(__builtin__, name)
    elif name in os.environ:
      return os.environ[name]
    else:
      raise NameError('name \'%s\' is not defined' % name)

  def evalArg(self, arg, globals, locals):
    w = StringIO.StringIO()
    for tok in arg:
      if tok[0] == LITERAL:
        w.write(tok[1])
      elif tok[0] == SINGLE_QUOTED_STRING:
        w.write(eval(tok[1]))
      elif tok[0] == SUBSTITUTION:
        w.write(str(self.evalSubstitution(tok[1], globals, locals)))
      else:
        raise Exception('Unexpected token: %s' % tok[0])
    return w.getvalue()
    
  def execute(self, globals, locals):
    #TODO: Supports redirect.
    pids = {}
    old_r = -1
    for proc in self.__parser.parse():
      is_last = proc.is_last
      args = []
      for arg in proc.args:
        args.append(self.evalArg(arg, globals, locals))
      redirects = []
      for redirect in proc.redirects:
        redirects.append((redirect[0],
                          self.evalArg(redirect[1], globals, locals)))
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
        if not is_last:
          os.dup2(w, sys.stdout.fileno())
        if old_r != -1:
          os.dup2(old_r, sys.stdin.fileno())
        for redirect in redirects:
          if redirect[0] == '>':
            mode = 'w'
          elif redirect[0] == '>>':
            mode = 'a'
          else:
            raise Exception('Unexpected error - '
                            'invalid redirect: %s' % redirect[0])
          f = file(redirect[1], mode)
          os.dup2(f.fileno(), sys.stdout.fileno())
        os.execvp(args[0], args)
    
    while len(pids) > 0:
      pid, rc = os.wait()
      w = pids.pop(pid)

def main():
  tok = Tokenizer('cat "$tmp/test.txt" | sed "s/e/*/g" > /tmp/out.txt')
  parser = Parser(tok)
  evaluator = Evaluator(parser)
  tmp = '/tmp'
  evaluator.execute(globals(), locals())

if __name__ == '__main__':
  main()