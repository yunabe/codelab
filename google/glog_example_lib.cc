#include <glog/logging.h>

int fib(int n) {
  VLOG(1) << "fib(" << n << ") is called.";
  if (n < 0) {
    LOG(FATAL) << "The parameter of fib (" << n << ") must not be negative.";
  } else if (n == 0) {
    return 0;
  } else if (n == 1) {
    return 1;
  } else {
    return fib(n - 1) + fib(n - 2);
  }
}
