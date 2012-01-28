import sys

import basic
import director

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


if __name__ == '__main__':
  main()
