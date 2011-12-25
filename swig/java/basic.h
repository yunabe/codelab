#include <string>
#include <vector>

namespace yunabe {
int int_sum(int x, int y);

std::string get_hello();

void dbl(int* n);

class Lib {
 public:
  static int int_mul(int x, int y);
};

class MyClass {
 public:
  MyClass(int x);

  int get_x();

 private:
  int x_;
};

}  // namespace yunabe
