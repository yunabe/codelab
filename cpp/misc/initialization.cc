// Learning C++ initialization.
// g++ initialization.cc -O3 -std=c++11 -o initialization && ./initialization

#include <iostream>

using namespace std;

// Actually, the only difference between struct and class in C++ is
// that members are public by default in struct and private in class.
// But I wrote both struct and class to confirm it.
struct S0 {
  int x;
  double y;
};

class C0 {
public:
  int x;
  double y;
};

struct S1 {
  int x;
  double get_y() const { return y; }
private:
  double y;
};

struct C1 {
public:
  int x;
  double get_y() const { return y; }
private:
  double y;
};

struct S2 {
  S2() : x(-1) {
    // x is initialized -1.
    // y is always uninitialized.
    cout << "S2::S2" << endl;
  }
  int x;
  double y;
};

class C2 {
public:
  C2() : x(-1) {
    // x is initialized -1.
    // y is always uninitialized.
    cout << "C2::C2" << endl;
  }
  int x;
  double y;
};

struct S3 {
  explicit S3(int val) : x(val) {
    // x is initialized val.
    // y is always uninitialized.
    cout << "S3::S3(" << val << ")" << endl;
  }
  int x;
  double y;
};

struct C3 {
  explicit C3(int val) : x(val) {
    // x is initialized val.
    // y is always uninitialized.
    cout << "C3::C3(" << val << ")" << endl;
  }
  int x;
  double y;
};

void learn_class_member_init() {
  cout << "#### learn_class_member_init ####" << endl;
  cout << "--- all public ---" << endl;
  {
    // Any x, y are not initialized (values are not defined).
    S0 s;
    C0 c;
    cout << "s.x: " << s.x << ", s.y: " << s.y << endl;
    cout << "c.x: " << c.x << ", c.y: " << c.y << endl;
  }
  {
    // All x, y are zero-initialized.
    S0 s{};
    C0 c{};
    cout << "s.x: " << s.x << ", s.y: " << s.y << endl;
    cout << "c.x: " << c.x << ", c.y: " << c.y << endl;
  }
  {
    S0 s{1};
    C0 c{1};
    // x is initialized with 1. y is zero-initialized.
    cout << "s.x: " << s.x << ", s.y: " << s.y << endl;
    cout << "c.x: " << c.x << ", c.y: " << c.y << endl;
  }
  {
    S0 s{3, 4};
    C0 c{3, 4};
    // x, y are initialized with 3, 4.
    cout << "s.x: " << s.x << ", s.y: " << s.y << endl;
    cout << "c.x: " << c.x << ", c.y: " << c.y << endl;
  }
  {
    // There are compile error.
    // S0 s();
    // C0 c();
  }
  cout << "--- with private ---" << endl;
  {
    S1 s;
    C1 c;
    // Any x, y are not initialized (values are not defined).
    cout << "s.x: " << s.x << ", s.y: " << s.get_y() << endl;
    cout << "c.x: " << c.x << ", c.y: " << c.get_y() << endl;
  }
  {
    S1 s{};
    C1 c{};
    // x, y are zero-initialized.
    cout << "s.x: " << s.x << ", s.y: " << s.get_y() << endl;
    cout << "c.x: " << c.x << ", c.y: " << c.get_y() << endl;
  }
  {
    // There are error because S1 and C1 have private members.
    // S1 s{1};
    // C1 c{1};
    // S1 s1{1, 2};
    // C1 c{1, 2};
  }
  {
    // There are compile errors.
    // S0 s();
    // C0 c();
  }
  cout << "--- with a constructor (no arg) ---" << endl;
  {
    S2 s;
    C2 c;
    // x is initialized. y is not.
    cout << "s.x: " << s.x << ", s.y: " << s.y << endl;
    cout << "c.x: " << c.x << ", c.y: " << c.y << endl;
  }
  {
    S2 s{};
    C2 c{};
    // x is initialized. y is not initialized in spite of {}.
    cout << "s.x: " << s.x << ", s.y: " << s.y << endl;
    cout << "c.x: " << c.x << ", c.y: " << c.y << endl;
  }
  {
    // There are error because S2 and C2 have constructor.
    // S2 s{1};
    // C2 c{1};
    // S2 s1{1, 2};
    // C2 c{1, 2};
  }
  cout << "--- with a constructor (with args) ---" << endl;
  {
    S3 s(3);
    C3 c(3);
    // x is initialized with 3. y is not initialized.
    cout << "s.x: " << s.x << ", s.y: " << s.y << endl;
    cout << "c.x: " << c.x << ", c.y: " << c.y << endl;
  }
  {
    // These also invoke constructors.
    S3 s{4};
    C3 c{4};
    // x is initialized with 3. y is not initialized in spite of {}.
    cout << "s.x: " << s.x << ", s.y: " << s.y << endl;
    cout << "c.x: " << c.x << ", c.y: " << c.y << endl;
  }
  {
    // Compile errors.
    // S3 s{};
    // C3 c{};
    // S3 s{1, 2};
    // C3 c{1, 2};
  }
}

int main(int argc, char** argv) {
  learn_class_member_init();
  return 0;
}
