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


if __name__ == '__main__':
  main()
