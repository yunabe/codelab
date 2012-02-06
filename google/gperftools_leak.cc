// Usage:
//   make gperftools_leak
//   HEAPCHECK=normal ./gperftools_leak
//
//   Memory leak is detected and an error message suggests you to run pprof.

#include <google/heap-checker.h>

void leak() {
  int* x = new int[100];
}

int main(int argc, char** argv) {
  leak();
  HeapLeakChecker::NoGlobalLeaks();
  return 0;
}
