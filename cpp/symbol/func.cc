// g++ -c -o func.o func.cc && nm func.o --demangle | grep -v use_symbols

// U (extern)
void func_decl();

// T (extern)
void func() {
}

// U (extern)
// warning. static is ignored if the func is not defined.
static void static_func_decl();

// t
static void static_func() {
}

void use_symbols() {
  // No symbol.
  static int static_var;
  // U
  // This is unusual. It's equivalent to extern outside of func as symbol.
  extern int extern_var;
  // Of course, no symbol.
  int local_var;
  ++static_var;
  ++extern_var;
  ++local_var;
  func_decl();
  func();
  static_func();
  static_func_decl();
}
