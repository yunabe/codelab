import unittest
import auto_property

class NameValidatorsTest(unittest.TestCase):
  def testIsGetterNameCapitalCamel(self):
    self.assertEqual('X',
                     auto_property.is_getter_name('GetX'));
    self.assertEqual('HttpHeader',
                     auto_property.is_getter_name('GetHttpHeader'));
    self.assertEqual('Y10',
                     auto_property.is_getter_name('GetY10'));
    self.assertEqual('Az0az',
                     auto_property.is_getter_name('GetAz0az'));
    self.assertEqual(None,
                     auto_property.is_getter_name('Getx'));

  def testIsGetterNameCamel(self):
    self.assertEqual('x',
                     auto_property.is_getter_name('getX'));
    self.assertEqual('httpHeader',
                     auto_property.is_getter_name('getHttpHeader'));
    self.assertEqual('y10',
                     auto_property.is_getter_name('getY10'));
    self.assertEqual('az0az',
                     auto_property.is_getter_name('getAz0az'));
    self.assertEqual(None,
                     auto_property.is_getter_name('getx'));

  def testIsGetterNameUnderscore(self):
    self.assertEqual('x',
                     auto_property.is_getter_name('get_x'));
    self.assertEqual('http_header',
                     auto_property.is_getter_name('get_http_header'));
    self.assertEqual('y10',
                     auto_property.is_getter_name('get_y10'));
    self.assertEqual('az0az',
                     auto_property.is_getter_name('get_az0az'));
    self.assertEqual('xx1_y2z',
                     auto_property.is_getter_name('get_xx1_y2z'));

  def testIsSetterNameCapitalCamel(self):
    self.assertEqual('X',
                     auto_property.is_setter_name('SetX'));
    self.assertEqual('HttpHeader',
                     auto_property.is_setter_name('SetHttpHeader'));
    self.assertEqual('Y10',
                     auto_property.is_setter_name('SetY10'));
    self.assertEqual('Az0az',
                     auto_property.is_setter_name('SetAz0az'));
    self.assertEqual(None,
                     auto_property.is_setter_name('Setx'));

  def testIsSetterNameCamel(self):
    self.assertEqual('x',
                     auto_property.is_setter_name('setX'));
    self.assertEqual('httpHeader',
                     auto_property.is_setter_name('setHttpHeader'));
    self.assertEqual('y10',
                     auto_property.is_setter_name('setY10'));
    self.assertEqual('az0az',
                     auto_property.is_setter_name('setAz0az'));
    self.assertEqual(None,
                     auto_property.is_setter_name('setx'));

  def testIsSetterNameUnderscore(self):
    self.assertEqual('x',
                     auto_property.is_setter_name('set_x'));
    self.assertEqual('http_header',
                     auto_property.is_setter_name('set_http_header'));
    self.assertEqual('y10',
                     auto_property.is_setter_name('set_y10'));
    self.assertEqual('az0az',
                     auto_property.is_setter_name('set_az0az'));
    self.assertEqual('xx1_y2z',
                     auto_property.is_setter_name('set_xx1_y2z'));

class AutoPropertyTest(unittest.TestCase):
  def testGetter(self):
    class C(object):
      __metaclass__ = auto_property.auto_property

      def get_x(self):
        return 123

    c = C()
    self.assertEqual(123, c.x)
    try:
      c.x = 3
      self.fail()
    except AttributeError:
      pass

  def testSetter(self):
    class C(object):
      __metaclass__ = auto_property.auto_property

      def __init__(self):
        self.value__ = ''

      def getValue(self):
        return '[' + self.value__ + ']'

      def setValue(self, value):
        self.value__ = value

    c = C()
    c.value = 'apple'
    self.assertEqual('[apple]', c.value)

  def testNoProperty(self):
    class C(object):
      __metaclass__ = auto_property.auto_property

      def __init__(self):
        self.c_internal = None
        self.d_internal = None

      @auto_property.not_accessor
      def getA(self):
        return 321

      def getB(self):
        return 777

      @auto_property.not_accessor
      def setC(self, value):
        self.c_internal = value

      def setD(self, value):
        self.d_internal = value

    c = C()
    self.assertFalse(hasattr(c, 'a'))
    self.assertTrue(hasattr(c, 'b'))
    self.assertEqual(777,
                     c.b)
    c.c = 10
    self.assertEqual(None, c.c_internal)
    c.d = 20
    self.assertEqual(20, c.d_internal)

if __name__ == '__main__':
  unittest.main()
