import re

__all__ = ['auto_property', 'not_accessor',]

CAMEL_NAME_PATTERN = '[A-Z][A-Za-z0-9]*'
UNDERSCORE_NAME_PATTERN = '[a-z][a-z0-9]*(_[a-z][a-z0-9]*)*'

GETTER_CAMEL_PATTERN = re.compile('^Get(%s)$' % CAMEL_NAME_PATTERN)
SETTER_CAMEL_PATTERN = re.compile('^Set(%s)$' % CAMEL_NAME_PATTERN)
GETTER_UNDERSCORE_PATTERN = re.compile('^get_(%s)$' % UNDERSCORE_NAME_PATTERN)
SETTER_UNDERSCORE_PATTERN = re.compile('^set_(%s)$' % UNDERSCORE_NAME_PATTERN)
GETTER_SMALL_CAMEL_PATTERN = re.compile('^get(%s)$' % CAMEL_NAME_PATTERN)
SETTER_SMALL_CAMEL_PATTERN = re.compile('^set(%s)$' % CAMEL_NAME_PATTERN)

def is_getter_name(name):
  m = GETTER_UNDERSCORE_PATTERN.match(name)
  if m:
    return m.group(1)
  m = GETTER_CAMEL_PATTERN.match(name)
  if m:
    return m.group(1)
  m = GETTER_SMALL_CAMEL_PATTERN.match(name)
  if m:
    # convert first character to lower case.
    return m.group(1)[0].lower() + m.group(1)[1:]
  return None

def is_setter_name(name):
  m = SETTER_UNDERSCORE_PATTERN.match(name)
  if m:
    return m.group(1)
  m = SETTER_CAMEL_PATTERN.match(name)
  if m:
    return m.group(1)
  m = SETTER_SMALL_CAMEL_PATTERN.match(name)
  if m:
    return m.group(1)[0].lower() + m.group(1)[1:]
  return None

class not_accessor(object):
  def __init__(self, function):
    self.function = function

class auto_property(type):
  def __new__(cls, classname, bases, dict):
    new_dict = {}
    setters = {}
    getters = {}
    properties = set()
    for name in dict:
      value = dict[name]
      if isinstance(value, not_accessor):
        new_dict[name] = value.function
        continue
      if not callable(value):
        new_dict[name] = value
        continue
      property_name = is_getter_name(name)
      if property_name:
        if property_name in getters:
          pass
        properties.add(property_name)
        getters[property_name] = value
        continue
      property_name = is_setter_name(name)
      if property_name:
        if property_name in setters:
          pass
        properties.add(property_name)
        setters[property_name] = value        
        continue
      new_dict[name] = value
    for property_name in properties:
      getter = getters.get(property_name, None)
      setter = setters.get(property_name, None)
      new_dict[property_name] = property(getter, setter)
    return type.__new__(cls, classname, bases, new_dict)
