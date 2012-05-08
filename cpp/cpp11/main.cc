#include <stdio.h>

int main(int argc, char** argv) {
  int x = 2;
  auto y = x;  // int y = x;
  auto& z = x;  // int& z = x;
  x = 3;
  printf("y == %d\n", y);
  printf("z == %d\n", z);
  return 0;
}
