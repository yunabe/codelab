%include "std_string.i"  // required to use std::string.
%include "typemaps.i"  // required to use INPUT/OUTPUT/INOUT.

%{
#include "basic.h"
%}

namespace yunabe {
int int_sum(int x, int y);

std::string get_hello();

void dbl(int* INOUT);

class Lib {
 public:
  static int int_mul(int x, int y);
};

class MyClass {
 public:
  MyClass(int x);

  %rename("getX") get_x();
  int get_x();
};

}  // namespace yunabe
