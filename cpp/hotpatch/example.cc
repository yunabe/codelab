#include <gflags/gflags.h>
#include <glog/logging.h>
#include <stdio.h>
#include <unistd.h>

#include "example_lib.h"

int main(int argc, char** argv) {
  google::InitGoogleLogging(argv[0]);
  google::ParseCommandLineFlags(&argc, &argv, true);
  int i = 0;
  while (true) {
    sleep(1);
    ++i;
    printf("i = %d [func(%d) = %d]\n", i, i, func(i));
  }
  return 0;
}
