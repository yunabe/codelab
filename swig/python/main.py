import sys

import time_type

# SWIG modules
import basic
import director
import use_time

class DirectorChild(director.DirectorRoot):
  def PrintName(self):
    print 'I\'m a child of DirectorRoot in Python!'


class NoDirectorChild(director.NoDirectorRoot):
  def PrintName(self):
    print 'I\'m a child of NoDirectorRoot in Python!'

class PythonSubtractor(use_time.Subtractor):
  def __init__(self):
    use_time.Subtractor.__init__(self)

  # if you forget 'self' here, swig outputs hard-to-understand error.
  # TODO: Understand what happends.
  def subtract(self, x, y):
    print 'Python: subtract %s from %s' % (y, x)
    return time_type.Time(x.hour - y.hour,
                          x.minute - y.minute,
                          x.second - y.second)


def main():
  print '---- Basic ---'
  print basic.get_hello()

  print '--- Director ---'

  d = DirectorChild()
  d.PrintName()

  # Overrided Java code are executed from C++
  # because it is declared as "director" in swig.
  director.DirectorRoot.CallPrintName(d)

  nod = NoDirectorChild()
  # Overrided Python code are executed.
  nod.PrintName()
  # Unfortunately, C++ codes of base class is called here.
  director.NoDirectorRoot.CallPrintName(nod)

  print '--- typemap ---'
  t0 = time_type.Time(1, 20, 30)
  t1 = time_type.Time(2, 40, 30)
  print use_time.sumTimeAsValue(t0, t1)

  print '--- typemap & director ---'
  sub = PythonSubtractor()
  # TODO: registerSubtractor must own ownership of sub.
  use_time.registerSubtractor(sub);
  print 'Python: The result is %s' % use_time.subtractTime(t1, t0)


if __name__ == '__main__':
  main()
