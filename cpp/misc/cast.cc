#include <iostream>

using namespace std;

class Parent {
public:
  virtual const char* name() {
    return "Parent";
  };
};

class Child0 : public Parent {
public:
  const char* name() override {
    return "Child0";
  };
};

class Child1 : public Parent {
public:
  const char* name() override {
    return "Child1";
  };
};

int main(int argc, char** argv) {
  //////////////////////////////////
  ////       static_cast        ////
  //////////////////////////////////
  // static_cast is used to write implicit
  // type-coversion explicitly.
  double d = 3.14;
  int i = static_cast<int>(d);
  // 1. Actually, implicit-conversion from double to int is allowed in C++.
  // int i = d;
  // 2. long l = static_cast<long>(&d); <-- compie error
  //    while `long l = (long)&d;` is valid (It's reinterpret_cast).
  cout << "i: " << i << endl;

  //////////////////////////////////
  ////       const_cast         ////
  //////////////////////////////////
  i  = 1000;
  const int *p = &i;
  // *p += 1; <-- compile error, of course.
  // int* q = p; <-- compile error too.

  // (Suprisingly?,) It is allowed to remove `const` with const_cast in C++.
  int* q = const_cast<int*>(p);
  *q += 1;
  cout << "*p: " << *p << endl;

  //////////////////////////////////
  ////       dynamic_cast       ////
  //////////////////////////////////
  Child0 child0;
  Parent* parent = &child0;
  // Child1* child1 = parent; <-- compile error.
  Child1* child1 = dynamic_cast<Child1*>(parent);
  Child0* child0_2 = dynamic_cast<Child0*>(parent);
  // child1 is nullptr. child0_2 == child0.
  cout << "child1: " << child1 << ", child0_2: " << child0_2 << endl;
  cout << "child0_2->name(): " << child0_2->name() << endl;

  //////////////////////////////////
  ////     reinterpret_cast     ////
  //////////////////////////////////
  int j;
  char* c = reinterpret_cast<char*>(&j);
  c[0] = 1;
  c[1] = 1;
  // 257 in little-endian.
  cout << "j: " << j << endl;
  long addrint = reinterpret_cast<long>(c);
  cout << "addrint: " << addrint << endl;
  // Note: reinterpret_cast<int>(c); causes a compile error.

  return 0;
}
