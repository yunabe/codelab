#include <string>
#include <stdio.h>
#include <thread>

using std::string;
using std::thread;

int SayHello(string name) {
  printf("Hello %s\n", name.c_str());
  return 1;  // The return value is ignored.
}

int main(int argc, char** argv) {
  std::thread th0(SayHello, "alice");
  std::thread th1(SayHello, "bob");
  th0.join();
  th1.join();
  return 0;
}
