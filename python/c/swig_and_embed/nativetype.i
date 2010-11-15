%module nativetype

%{
#include "nativetype.h"

// A function to wrap existing native instance.
// We can know how to wrap instance from auto-generated code for Root::get_left.
PyObject* wrapRootInstance(const Root& root) {
  return SWIG_NewPointerObj(SWIG_as_voidptr(&root), SWIGTYPE_p_Root, 0 |  0 );
};

%}

%nodefaultctor Root;
%nodefaultdtor Root;
class Root {
 public:
  const Leaf& get_left() { return left_; };
  const Leaf& get_right() { return right_; };
};

%nodefaultctor Leaf;
%nodefaultdtor Leaf;
class Leaf {
 public:
  int get_value() { return value_ };
};
