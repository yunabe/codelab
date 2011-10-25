#include <stdio.h>
#include <stdlib.h>

int fib(int n);

int main(int argc, char** argv) {
  int n = 0;
  if (argc == 2) {
    n = atoi(argv[1]);
  }
  if (n == 0) {
    n = 40;
  }
  printf("fib(%d) = %d\n", n, fib(n));
  return 0;
}
