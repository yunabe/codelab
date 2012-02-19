import tokenize
import token
import StringIO

SPACE = 'space'
SINGLE_QUOTED_STRING = 'single_quoted'
DOUBLE_QUOTED_STRING = 'double_quoted'
SUBSTITUTION = 'substitution'
REDIRECT = 'redirect'
PIPE = 'pipe'
LITERAL = 'literal'

class Tokenizer(object):
  def __init__(self, input):
    self.__input = input.strip()

  def __iter__(self):
    return self

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

  def find_char(self, s, cond):
    for i, c in enumerate(s):
      if cond(c):
        return i
    return -1

  def extract_string(self, input):
    toks = tokenize.generate_tokens(StringIO.StringIO(input).readline)
    tok = toks.next()
    if tok[0] == token.STRING:
      return tok[1]
    else:
      raise Exception('Wrong string format')

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

  def next(self):
    input = self.__input
    if not input:
      raise StopIteration()

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

def main():
  tok = Tokenizer('cat ~/www/foo.txt  "a b" ${var}1 | '
                  'grep bar 2> &1 > /tmp/baz.txt')
  print list(tok)

if __name__ == '__main__':
  main()
