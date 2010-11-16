#include <dlfcn.h>
#include <stdio.h>
#include <string>

using std::string;

void load_and_invoke(const string& lib, const string& method, int x, int y) {
  void *handle;
  void (*func)(int, int);
  char *error;
  // Open the shared object
  handle = dlopen(lib.c_str(), RTLD_LAZY );
  if (!handle) {
    printf( "%s\n", dlerror() );
    return;
  }
  // Resolve the symbol from the object
  func = (void (*)(int, int))dlsym(handle, method.c_str());
  error = dlerror();
  if (error != NULL) {
    printf( "%s\n", error );
    return;
  }
  // Call the resolved method
  (*func)(x, y);
  // Close the object
  dlclose(handle);
}

void show_result(int n) {
  printf("result = %d\n", n);
}

int main(int argc, char** argv) {
  // If filename contains a slash ("/"), then it is interpreted as a pathname.
  // Otherwise, searches for shared libraries in an usual way
  // (from LD_LIBRARY_PATH, /usr/lib/, etc...)
  load_and_invoke("./func_add.so", "func", 3, 4);
  // No problem even if another shared library uses a same name.
  load_and_invoke("./func_mul.so", "func", 3, 4);
  // Invalid library name.
  load_and_invoke("dummy.so", "func", 3, 4);
  // Invalid symbol name.
  load_and_invoke("./func_mul.so", "dummy", 3, 4);
  return 0;
}
