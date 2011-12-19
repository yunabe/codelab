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

  public static int[] reverseIntArray(int[] array) {
    int[] result = new int[array.length];
    for (int i = 0; i < array.length; ++i) {
      result[array.length - 1 - i] = array[i];
    }
    return result;
  }
}

