// g++ -c -o global.o global.cc -fpermissive
// nm global.o --demangle | grep -v use_symbols

// "B" (extern)
int uninitialized;
// "U" (extern)
extern int extern_uninitialized;
// "b"
static int static_uninitialized;

// "D" (extern)
int initialized = 10;
// "D" (extern)
extern int extern_initialized = 20;
// "d"
static int static_initialized = 30;

// "b"
const int const_uninitialized;  // compile error
// "U" (extern)
const extern int const_extern_uninitialized;
// "b"
const static int const_static_uninitialized;  // compile error

// "r"
const int const_initialized = 10;
// "R" (extern)
const extern int const_extern_initialized = 20;
// "r"
const static int const_static_initialized = 30;

int use_symbols() {
  return uninitialized +
    extern_uninitialized +
    static_uninitialized +
    initialized +
    extern_initialized +
    static_initialized +
    const_uninitialized +
    const_extern_uninitialized +
    const_static_uninitialized +
    const_initialized +
    const_extern_initialized +
    const_static_initialized;
}
