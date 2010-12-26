#include <stdio.h>

#include "sample.h"

const char* message = " was updated.";

Sample::Sample(int x, int y) : x_(x), y_(y) {
  printf("Sample::Sample %s\n", message);
}

Sample::~Sample() {
  printf("Sample::~Sample %s\n", message);
}

int Sample::method() {
  printf("Sample::medhod %s\n", message);
  return x_ + y_;
}

int Sample::virtual_method() {
  printf("Sample::virtual_medhod %s\n", message);
  return x_ * y_;
}
