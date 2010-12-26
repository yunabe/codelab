#include <stdio.h>
#include <unistd.h>
#include <string>

#include "dynamic_update.h"
#include "sample.h"

int main(int argc, char** argv) {
  for (int i = 0;; ++i) {
    if (i > 0) {
      printf("\n");
    }
    printf("**** loop i = %d ****\n", i);
    Sample s(3, 4);
    printf("s.method() = %d\n", s.method());
    printf("s.virtual_method() = %d\n", s.virtual_method());
    string error;
    if (!UpdateLibrary("./new_sample.so", &error)) {
      printf("Failed to UpdateLibrary: %s\n", error.c_str());
    }
    sleep(2);
  }
}
