void show_result(int n);

extern "C" {
  void func(int x, int y) {
    show_result(x * y);
  }
}
