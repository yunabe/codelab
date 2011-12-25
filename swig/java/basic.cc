#include "basic.h"

namespace yunabe {

int int_sum(int x, int y) {
  return x + y;
}

std::string get_hello() {
  // Should be UTF8.
  return "こんにちは世界!";
}

int Lib::int_mul(int x, int y) {
  return x * y;
}

}  // namespace yunabe
