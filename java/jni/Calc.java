public class Calc {
  public static int sum(int x, int y) {
    return x + y;
  }

  public static void throw_exception() {
    throw_exception_internal();
  }

  private static void throw_exception_internal() {
    throw new RuntimeException("Hello exception!");
  }
}
