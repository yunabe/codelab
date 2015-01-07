#include <stdio.h>
#include <functional>

class Wrapper {
 public:
  Wrapper(int v) : value(v) {};
  Wrapper(const Wrapper& w) : value(w.value) {
    printf("copy: %d\n", w.value);
  };

  int value;
};

std::function<int(int)> hoge(int n) {
  Wrapper w(n);
  //  [w] must not be [&w] because the life time of w is this function scope.
  std::function<int(int)> func = [w](int x) { return x + w.value; };
  return func;
}

void basic() {
  int m = 1;
  int n = 2;
  auto f = [m, &n]() -> void {printf("m == %d, n == %d\n", m, n);};
  n = 3;
  f();
  auto sum = [](int x, int y) { return x + y; };
  printf("sum(3, 4) == %d\n", sum(3, 4));

  auto plus5 = hoge(5);
  auto plus7 = hoge(7);
  printf("plus5(3) == %d\n", plus5(3));
  printf("plus7(3) == %d\n", plus7(3));
}

int main(int argc, char** argv) {
  basic();
  return 0;
}
