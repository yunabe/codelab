#include "basic.h"

namespace yunabe {

int int_sum(int x, int y) {
  return x + y;
}

void dbl(int* n) {
  *n = (*n) * 2;
}

std::string get_hello() {
  // Should be UTF8.
  return "こんにちは世界!";
}

int Lib::int_mul(int x, int y) {
  return x * y;
}

}  // namespace yunabe
