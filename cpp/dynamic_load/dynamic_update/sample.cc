#include "sample.h"

Sample::Sample(int x, int y) : x_(x), y_(y) {
}

Sample::~Sample() {
}

int Sample::method() {
  return x_ + y_;
}

int Sample::virtual_method() {
  return x_ * y_;
}
