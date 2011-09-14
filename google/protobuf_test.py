import unittest

import example_pb2
from google.protobuf import text_format


def RemoveSpaces(s):
  return s.replace(' ', '').replace('\n', '')


class TestProtobuf(unittest.TestCase):
  def testDefault(self):
    p = example_pb2.Person()
    p.name = 'Taro'
    b = p.birthday
    b.year = 1999
    b.month = 1
    b.day = 2
    attr = p.attribute.add()
    attr.name = 'key'
    attr.value = 'val'
    self.assertEqual(RemoveSpaces(text_format.MessageToString(p)),
                     RemoveSpaces('name: "Taro"'
                                  '  birthday {'
                                  '  year: 1999'
                                  '  month: 1'
                                  '  day: 2'
                                  '}'
                                  'attribute {'
                                  '  name: "key"'
                                  '  value: "val"'
                                  '}'))

if __name__ == '__main__':
  unittest.main()
